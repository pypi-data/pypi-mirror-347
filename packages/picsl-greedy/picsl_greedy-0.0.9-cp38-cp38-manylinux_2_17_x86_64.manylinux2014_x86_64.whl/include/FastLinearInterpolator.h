/*=========================================================================

  Program:   ALFABIS fast medical image registration programs
  Language:  C++
  Website:   github.com/pyushkevich/greedy
  Copyright (c) Paul Yushkevich, University of Pennsylvania. All rights reserved.

  This program is part of ALFABIS: Adaptive Large-Scale Framework for
  Automatic Biomedical Image Segmentation.

  ALFABIS development is funded by the NIH grant R01 EB017255.

  ALFABIS is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  ALFABIS is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with ALFABIS.  If not, see <http://www.gnu.org/licenses/>.

=========================================================================*/
#ifndef __FastLinearInterpolator_h_
#define __FastLinearInterpolator_h_

#include "itkImage.h"
#include "itkVectorImage.h"
#include "itkNumericTraits.h"
#include "itkNumericTraitsCovariantVectorPixel.h"

template <class TFloat, class TInputComponentType>
struct FastLinearInterpolatorOutputTraits
{
};

template <class TInputComponentType>
struct FastLinearInterpolatorOutputTraits<float, TInputComponentType>
{
  typedef typename itk::NumericTraits<TInputComponentType>::FloatType OutputComponentType;
};

template <class TInputComponentType>
struct FastLinearInterpolatorOutputTraits<double, TInputComponentType>
{
  typedef typename itk::NumericTraits<TInputComponentType>::RealType OutputComponentType;
};

template <class TImageType>
struct FastWarpCompositeImageFilterInputImageTraits
{
};

template <class TPixel, unsigned int VDim>
struct FastWarpCompositeImageFilterInputImageTraits< itk::Image<TPixel, VDim> >
{
  static int GetPointerIncrementSize(const itk::Image<TPixel, VDim> *) { return 1; }
};

template <class TPixel, unsigned int VDim>
struct FastWarpCompositeImageFilterInputImageTraits< itk::VectorImage<TPixel, VDim> >
{
  static int GetPointerIncrementSize(const itk::VectorImage<TPixel, VDim> *image)
  {
    return image->GetNumberOfComponentsPerPixel();
  }
};

template <class TAtomic, class TReal>
struct LinearInterpolateImpl
{
  static void lerp(TReal a, const TAtomic &l, const TAtomic &h, TAtomic &result)
  {
    result = l+((h-l)*a);
  }
};

template <class TReal>
struct LinearInterpolateImpl<itk::CovariantVector<TReal, 2>, TReal>
{
  typedef itk::CovariantVector<TReal, 2> Vec;
  static void lerp(TReal a, const Vec &l, const Vec &h, Vec &result)
  {
    result[0] = l[0] + ((h[0] - l[0]) * a);
    result[1] = l[1] + ((h[1] - l[1]) * a);
  }
};

template <class TReal>
struct LinearInterpolateImpl<itk::CovariantVector<TReal, 3>, TReal>
{
  typedef itk::CovariantVector<TReal, 3> Vec;
  static void lerp(TReal a, const Vec &l, const Vec &h, Vec &result)
  {
    result[0] = l[0] + ((h[0] - l[0]) * a);
    result[1] = l[1] + ((h[1] - l[1]) * a);
    result[2] = l[2] + ((h[2] - l[2]) * a);
  }
};

/**
 * Base class for the fast linear interpolators
 */
template<class TImage, class TFloat, unsigned int VDim,
         class TMaskImage = itk::Image<float, VDim> >
class FastLinearInterpolatorBase
{
public:
  typedef TImage                                                  ImageType;
  typedef TMaskImage                                              MaskImageType;
  typedef TFloat                                                  RealType;
  typedef typename MaskImageType::PixelType                       MaskPixelType;
  typedef typename ImageType::InternalPixelType                   InputComponentType;
  typedef FastLinearInterpolatorOutputTraits<TFloat, InputComponentType>  OutputTraits;
  typedef typename OutputTraits::OutputComponentType              OutputComponentType;
  typedef typename itk::ImageRegion<VDim>                         RegionType;

  /** Determine the image dimension. */
  itkStaticConstMacro(ImageDimension, unsigned int, ImageType::ImageDimension );

  enum InOut { INSIDE = 0, OUTSIDE, BORDER };

  /**
   * Get the number that should be added to the input pointer when parsing the input and
   * output images. This will be 1 for itk::Image and Ncomp for itk::VectorImage
   */
  int GetPointerIncrement() const { return nComp; }

  FastLinearInterpolatorBase(ImageType *image, const RegionType &region, MaskImageType *mask = NULL)
  {
    nComp = FastWarpCompositeImageFilterInputImageTraits<TImage>::GetPointerIncrementSize(image);
    auto region_offset = nComp * image->ComputeOffset(region.GetIndex());
    buffer = image->GetBufferPointer() + region_offset;
    def_value_store = new InputComponentType[nComp];
    for(int i = 0; i < nComp; i++)
      def_value_store[i] = itk::NumericTraits<InputComponentType>::ZeroValue();
    def_value = def_value_store;

    // Store the moving mask pointer
    mask_buffer = mask ? mask->GetBufferPointer() : NULL;
  }

  ~FastLinearInterpolatorBase()
  {
    delete [] def_value_store;
  }

  void SetOutsideValue(InputComponentType value)
    {
    for(int i = 0; i < nComp; i++)
      def_value_store[i] = value;
    }

protected:


  int nComp;
  const InputComponentType *buffer;
  const MaskPixelType *mask_buffer;

  // Default value - for interpolation outside of the image bounds
  const InputComponentType *def_value;
  InputComponentType *def_value_store;

  InOut status;
};


/**
 * Arbitrary dimension fast linear interpolator - meant to be slow
 */
template<class TImage, class TFloat, unsigned int VDim,
         class TMaskImage = itk::Image<float, VDim> >
class FastLinearInterpolator : public FastLinearInterpolatorBase<TImage, TFloat, VDim, TMaskImage>
{
public:
  typedef FastLinearInterpolatorBase<TImage, TFloat, VDim, TMaskImage>   Superclass;
  typedef typename Superclass::ImageType               ImageType;
  typedef typename Superclass::MaskImageType           MaskImageType;
  typedef typename Superclass::InputComponentType      InputComponentType;
  typedef typename Superclass::OutputComponentType     OutputComponentType;
  typedef typename Superclass::RealType                RealType;
  typedef typename Superclass::InOut                   InOut;
  typedef typename Superclass::RegionType              RegionType;

  FastLinearInterpolator(ImageType *image, MaskImageType *mask = nullptr)
    : FastLinearInterpolator(image, image->GetLargestPossibleRegion(), mask) {}

  FastLinearInterpolator(ImageType *image, const RegionType &region, MaskImageType *mask = nullptr)
    : Superclass(image, region, mask) {}

  InOut InterpolateWithGradient(RealType *itkNotUsed(cix), OutputComponentType *itkNotUsed(out), OutputComponentType **itkNotUsed(grad))
    { return Superclass::INSIDE; }

  InOut Interpolate(RealType *itkNotUsed(cix), OutputComponentType *itkNotUsed(out))
    { return Superclass::INSIDE; }

  InOut InterpolateNearestNeighbor(RealType *itkNotUsed(cix), OutputComponentType *itkNotUsed(out))
    { return Superclass::INSIDE; }

  TFloat GetMask() { return 0.0; }

  TFloat GetMaskAndGradient(RealType *itkNotUsed(mask_gradient)) { return 0.0; }

  InOut Splat(RealType *itkNotUsed(cix), const InputComponentType *itkNotUsed(value))
    { return Superclass::INSIDE; }

  void GetIndexAndRemainer(int *itkNotUsed(index), RealType *itkNotUsed(remainder)) { }

  template <class THistContainer>
  void PartialVolumeHistogramSample(RealType *itkNotUsed(cix),
                                    const InputComponentType *itkNotUsed(fixptr),
                                    THistContainer &itkNotUsed(hist)) {}

  template <class THistContainer>
  void PartialVolumeHistogramGradientSample(RealType *itkNotUsed(cix),
                                            const InputComponentType *itkNotUsed(fix_ptr),
                                            const THistContainer &itkNotUsed(hist_w),
                                            RealType *itkNotUsed(out_grad)) {}

protected:
};

/**
 * 3D fast linear interpolator - optimized for speed
 */
template <class TImage, class TFloat, class TMaskImage>
class FastLinearInterpolator<TImage, TFloat, 3, TMaskImage>
    : public FastLinearInterpolatorBase<TImage, TFloat, 3, TMaskImage>
{
public:
  typedef TImage                                                           ImageType;
  typedef TMaskImage                                                       MaskImageType;
  typedef FastLinearInterpolatorBase<ImageType, TFloat, 3, MaskImageType>  Superclass;
  typedef typename Superclass::InputComponentType                          InputComponentType;
  typedef typename Superclass::OutputComponentType                         OutputComponentType;
  typedef typename Superclass::RealType                                    RealType;
  typedef typename Superclass::InOut                                       InOut;
  typedef typename Superclass::MaskPixelType                               MaskPixelType;
  typedef typename Superclass::RegionType                                  RegionType;
  typedef LinearInterpolateImpl<OutputComponentType, RealType>             LERP;
  typedef LinearInterpolateImpl<RealType, RealType>                        MLERP;


  FastLinearInterpolator(ImageType *image, const RegionType &region, MaskImageType *mask = nullptr) : Superclass(image, region, mask)
  {
    xind = region.GetIndex()[0];
    yind = region.GetIndex()[1];
    zind = region.GetIndex()[2];

    xsize = region.GetSize()[0];
    ysize = region.GetSize()[1];
    zsize = region.GetSize()[2];

    off_x = this->nComp;
    off_y = xsize * off_x;
    off_z = ysize * off_y;
    off_mz = ysize * xsize;
  }

  FastLinearInterpolator(ImageType *image, MaskImageType *mask = NULL) : FastLinearInterpolator(image, image->GetLargestPossibleRegion(), mask) {}

  /**
   * Compute the pointers to the eight corners of the interpolating cube
   */
  InOut ComputeCorners(RealType *cix)
  {
    // Split index into floor and remainder
    RealType fl_cx = floor(cix[0]);
    RealType fl_cy = floor(cix[1]);
    RealType fl_cz = floor(cix[2]);
    fx = cix[0] - fl_cx;
    fy = cix[1] - fl_cy;
    fz = cix[2] - fl_cz;
    x0 = ((int) fl_cx) - xind;
    y0 = ((int) fl_cy) - yind;
    z0 = ((int) fl_cz) - zind;

    // Adjust for non-zero index
    /*
    RealType px = cix[0] - xind, py = cix[1] - yind, pz = cix[2] - zind;

    x0 = (int) floor(px); fx = px - x0;
    y0 = (int) floor(py); fy = py - y0;
    z0 = (int) floor(pz); fz = pz - z0; */

    x1 = x0 + 1;
    y1 = y0 + 1;
    z1 = z0 + 1;

    if (x0 >= 0 && x1 < xsize &&
        y0 >= 0 && y1 < ysize &&
        z0 >= 0 && z1 < zsize)
      {
      // The sample point is completely inside
      d000 = dens(x0, y0, z0);
      d100 = d000 + off_x;
      d010 = d000 + off_y;
      d110 = d010 + off_x;
      d001 = d000 + off_z;
      d101 = d001 + off_x;
      d011 = d010 + off_z;
      d111 = d011 + off_x;

      // Is there a mask? If so, sample the mask
      if(this->mask_buffer)
        {
        // Sample the mask
        const MaskPixelType *mp = mens(x0, y0, z0);

        m000 = *mp;
        m100 = *(mp+1);
        mp += xsize;
        m010 = *mp;
        m110 = *(mp+1);
        mp += off_mz;
        m011 = *mp;
        m111 = *(mp+1);
        mp -= xsize;
        m001 = *mp;
        m101 = *(mp+1);

        // Check the mask - if != 1 for any pixel, this is considered a border pixel
        if(m000 == 1 && m001 == 1 && m010 == 1 && m011 == 1 &&
           m100 == 1 && m101 == 1 && m110 == 1 && m111 == 1)
          {
          this->status = Superclass::INSIDE;
          }
        else if (m000 == 0 && m001 == 0 && m010 == 0 && m011 == 0 &&
                 m100 == 0 && m101 == 0 && m110 == 0 && m111 == 0)
          {
          this->status = Superclass::OUTSIDE;
          }
        else
          {
          this->status = Superclass::BORDER;
          }
        }
      else
        {
        // The mask is one
        this->status = Superclass::INSIDE;
        }
      }
    else if (x0 >= -1 && x1 <= xsize &&
             y0 >= -1 && y1 <= ysize &&
             z0 >= -1 && z1 <= zsize)
      {
      // The sample point is on the border region
      d000 = border_check(x0, y0, z0, m000);
      d001 = border_check(x0, y0, z1, m001);
      d010 = border_check(x0, y1, z0, m010);
      d011 = border_check(x0, y1, z1, m011);
      d100 = border_check(x1, y0, z0, m100);
      d101 = border_check(x1, y0, z1, m101);
      d110 = border_check(x1, y1, z0, m110);
      d111 = border_check(x1, y1, z1, m111);

      if(this->mask_buffer &&
         (m000 == 0 && m001 == 0 && m010 == 0 && m011 == 0 &&
          m100 == 0 && m101 == 0 && m110 == 0 && m111 == 0))
        this->status = Superclass::OUTSIDE;
      else
        this->status = Superclass::BORDER;
      }
    else
      {
      // The mask is zero
      this->status = Superclass::OUTSIDE;
      }

    return this->status;
  }

  void GetIndexAndRemainer(int *index, RealType *remainder)
  {
    index[0] = this->x0; index[1] = this->y0; index[2] = this->z0;
    remainder[0] = this->fx; remainder[1] = this->fy; remainder[2] = this->fz;
  }

  /**
   * Interpolate at position cix, placing the intensity values in out and gradient
   * values in grad (in strides of VDim)
   */
  InOut InterpolateWithGradient(RealType *cix, OutputComponentType *out, OutputComponentType **grad)
  {
    OutputComponentType dx00, dx01, dx10, dx11, dxy0, dxy1;
    OutputComponentType dx00_x, dx01_x, dx10_x, dx11_x, dxy0_x, dxy1_x;
    OutputComponentType dxy0_y, dxy1_y;

    // Compute the corners
    this->ComputeCorners(cix);

    if(this->status != Superclass::OUTSIDE)
      {
      // Loop over the components
      for(int iComp = 0; iComp < this->nComp; iComp++, grad++,
          d000++, d001++, d010++, d011++,
          d100++, d101++, d110++, d111++)
        {
        // Interpolate the image intensity
        LERP::lerp(fx, *d000, *d100, dx00);
        LERP::lerp(fx, *d001, *d101, dx01);
        LERP::lerp(fx, *d010, *d110, dx10);
        LERP::lerp(fx, *d011, *d111, dx11);
        LERP::lerp(fy, dx00, dx10, dxy0);
        LERP::lerp(fy, dx01, dx11, dxy1);
        LERP::lerp(fz, dxy0, dxy1, *(out++));

        // Interpolate the gradient in x
        dx00_x = *d100 - *d000;
        dx01_x = *d101 - *d001;
        dx10_x = *d110 - *d010;
        dx11_x = *d111 - *d011;
        LERP::lerp(fy, dx00_x, dx10_x, dxy0_x);
        LERP::lerp(fy, dx01_x, dx11_x, dxy1_x);
        LERP::lerp(fz, dxy0_x, dxy1_x, (*grad)[0]);

        // Interpolate the gradient in y
        dxy0_y = dx10 - dx00;
        dxy1_y = dx11 - dx01;
        LERP::lerp(fz, dxy0_y, dxy1_y, (*grad)[1]);

        // Interpolate the gradient in z
        (*grad)[2] = dxy1 - dxy0;
        }
      }

    return this->status;
  }

  InOut Interpolate(RealType *cix, OutputComponentType *out)
  {
    OutputComponentType dx00, dx01, dx10, dx11, dxy0, dxy1;

    // Compute the corners
    this->ComputeCorners(cix);

    if(this->status != Superclass::OUTSIDE)
      {
      // Loop over the components
      for(int iComp = 0; iComp < this->nComp; iComp++,
          d000++, d001++, d010++, d011++,
          d100++, d101++, d110++, d111++)
        {
        // Interpolate the image intensity
        LERP::lerp(fx, *d000, *d100, dx00);
        LERP::lerp(fx, *d001, *d101, dx01);
        LERP::lerp(fx, *d010, *d110, dx10);
        LERP::lerp(fx, *d011, *d111, dx11);
        LERP::lerp(fy, dx00, dx10, dxy0);
        LERP::lerp(fy, dx01, dx11, dxy1);
        LERP::lerp(fz, dxy0, dxy1, *(out++));
        }
      }

    return this->status;
  }

  InOut InterpolateNearestNeighbor(RealType *cix, OutputComponentType *out)
  {
    // Adjust for non-zero index
    RealType px = cix[0] - xind, py = cix[1] - yind, pz = cix[2] - zind;
    x0 = (int) floor(px + 0.5);
    y0 = (int) floor(py + 0.5);
    z0 = (int) floor(pz + 0.5);

    if (x0 >= 0 && x0 < xsize &&
        y0 >= 0 && y0 < ysize &&
        z0 >= 0 && z0 < zsize)
      {
      const InputComponentType *dp = dens(x0, y0, z0);
      for(int iComp = 0; iComp < this->nComp; iComp++)
        {
        out[iComp] = dp[iComp];
        }
      return Superclass::INSIDE;
      }
    else return Superclass::OUTSIDE;
  }

  InOut Splat(RealType *cix, const InputComponentType *value)
  {
    // Compute the corners
    this->ComputeCorners(cix);

    // When inside, no checks are required
    if(this->status != Superclass::OUTSIDE)
      {
      // Compute the corner weights using 4 multiplications (not 16)
      RealType fxy = fx * fy, fyz = fy * fz, fxz = fx * fz, fxyz = fxy * fz;

      RealType w111 = fxyz;
      RealType w011 = fyz - fxyz;
      RealType w101 = fxz - fxyz;
      RealType w110 = fxy - fxyz;
      RealType w001 = fz - fxz - w011;
      RealType w010 = fy - fyz - w110;
      RealType w100 = fx - fxy - w101;
      RealType w000 = 1.0 - fx - fy + fxy - w001;

      // Loop over the components
      if(this->status == Superclass::INSIDE)
        {
        for(int iComp = 0; iComp < this->nComp; iComp++,
            d000++, d001++, d010++, d011++,
            d100++, d101++, d110++, d111++, value++)
          {
          // Assign the appropriate weight to each part of the histogram
          InputComponentType val = *value;
          *const_cast<InputComponentType *>(d000) += w000 * val;
          *const_cast<InputComponentType *>(d001) += w001 * val;
          *const_cast<InputComponentType *>(d010) += w010 * val;
          *const_cast<InputComponentType *>(d011) += w011 * val;
          *const_cast<InputComponentType *>(d100) += w100 * val;
          *const_cast<InputComponentType *>(d101) += w101 * val;
          *const_cast<InputComponentType *>(d110) += w110 * val;
          *const_cast<InputComponentType *>(d111) += w111 * val;
          }
        }
      else
        {
        // Border case - special checks
        auto *dv = this->def_value;
        for(int iComp = 0; iComp < this->nComp; iComp++,
            d000++, d001++, d010++, d011++,
            d100++, d101++, d110++, d111++, value++, dv++)
          {
          // Assign the appropriate weight to each part of the histogram
          InputComponentType val = *value;
          if(d000 != dv) *const_cast<InputComponentType *>(d000) += w000 * val;
          if(d001 != dv) *const_cast<InputComponentType *>(d001) += w001 * val;
          if(d010 != dv) *const_cast<InputComponentType *>(d010) += w010 * val;
          if(d011 != dv) *const_cast<InputComponentType *>(d011) += w011 * val;
          if(d100 != dv) *const_cast<InputComponentType *>(d100) += w100 * val;
          if(d101 != dv) *const_cast<InputComponentType *>(d101) += w101 * val;
          if(d110 != dv) *const_cast<InputComponentType *>(d110) += w110 * val;
          if(d111 != dv) *const_cast<InputComponentType *>(d111) += w111 * val;
          }
        }
      }

    return this->status;
  }

  template <class THistContainer>
  void PartialVolumeHistogramSample(RealType *cix, const InputComponentType *fixptr, THistContainer &hist)
  {
    // Compute the corners
    this->ComputeCorners(cix);

    if(this->status != Superclass::OUTSIDE)
      {
      // Compute the corner weights using 4 multiplications (not 16)
      RealType fxy = fx * fy, fyz = fy * fz, fxz = fx * fz, fxyz = fxy * fz;

      RealType w111 = fxyz;
      RealType w011 = fyz - fxyz;
      RealType w101 = fxz - fxyz;
      RealType w110 = fxy - fxyz;
      RealType w001 = fz - fxz - w011;
      RealType w010 = fy - fyz - w110;
      RealType w100 = fx - fxy - w101;
      RealType w000 = 1.0 - fx - fy + fxy - w001;

      // Loop over the components
      for(int iComp = 0; iComp < this->nComp; iComp++,
          d000++, d001++, d010++, d011++,
          d100++, d101++, d110++, d111++, fixptr++)
        {
        // Just this line in the histogram
        RealType *hist_line = hist[iComp][*fixptr];

        // Assign the appropriate weight to each part of the histogram
        hist_line[*d000] += w000;
        hist_line[*d001] += w001;
        hist_line[*d010] += w010;
        hist_line[*d011] += w011;
        hist_line[*d100] += w100;
        hist_line[*d101] += w101;
        hist_line[*d110] += w110;
        hist_line[*d111] += w111;
        }
      }
    else
      {
      for(int iComp = 0; iComp < this->nComp; iComp++, fixptr++)
        {
        // Just this line in the histogram
        RealType *hist_line = hist[iComp][*fixptr];
        hist_line[0] += 1.0;
        }
      }
  }

  template <class THistContainer>
  void PartialVolumeHistogramGradientSample(RealType *cix, const InputComponentType *fixptr, const THistContainer &hist_w, RealType *out_grad)
  {
    // Compute the corners
    this->ComputeCorners(cix);

    // Outside values do not contribute to the gradient
    if(this->status != Superclass::OUTSIDE)
      {
      // Compute the corner weights using 4 multiplications (not 16)
      RealType fxy = fx * fy, fyz = fy * fz, fxz = fx * fz;

      // Some horrendous derivatives here! Wow!
      RealType w111x = fyz,             w111y = fxz,             w111z = fxy;
      RealType w011x = -fyz,            w011y = fz - fxz,        w011z = fy - fxy;
      RealType w101x = fz - fyz,        w101y = -fxz,            w101z = fx - fxy;
      RealType w110x = fy - fyz,        w110y = fx - fxz,        w110z = -fxy;
      RealType w001x = -fz - w011x,     w001y = -w011y,          w001z = 1 - fx - w011z;
      RealType w010x = -w110x,          w010y = 1 - fz - w110y,  w010z = -fy - w110z;
      RealType w100x = 1 - fy - w101x,  w100y = -fx - w101y,     w100z = -w101z;
      RealType w000x = -1 + fy - w001x, w000y = -1 + fx - w001y, w000z = -w001z;

      // Initialize gradient to zero
      out_grad[0] = 0.0;
      out_grad[1] = 0.0;
      out_grad[2] = 0.0;

      // Loop over the components
      for(int iComp = 0; iComp < this->nComp; iComp++,
          d000++, d001++, d010++, d011++,
          d100++, d101++, d110++, d111++, fixptr++)
        {
        // Just this line in the histogram
        const RealType *f = hist_w[iComp][*fixptr];

        // Take the weighted sum
        RealType f000 = f[*d000], f001 = f[*d001], f010 = f[*d010], f011 = f[*d011];
        RealType f100 = f[*d100], f101 = f[*d101], f110 = f[*d110], f111 = f[*d111];

        out_grad[0] += w000x * f000 + w001x * f001 + w010x * f010 + w011x * f011 +
                       w100x * f100 + w101x * f101 + w110x * f110 + w111x * f111;

        out_grad[1] += w000y * f000 + w001y * f001 + w010y * f010 + w011y * f011 +
                       w100y * f100 + w101y * f101 + w110y * f110 + w111y * f111;

        out_grad[2] += w000z * f000 + w001z * f001 + w010z * f010 + w011z * f011 +
                       w100z * f100 + w101z * f101 + w110z * f110 + w111z * f111;
        }
      }
    else
      {
      out_grad[0] = 0.0;
      out_grad[1] = 0.0;
      out_grad[2] = 0.0;
      }
  }

  RealType GetMask()
  {
    // Interpolate the mask
    RealType dx00, dx01, dx10, dx11, dxy0, dxy1, mask;
    MLERP::lerp(fx, m000, m100, dx00);
    MLERP::lerp(fx, m001, m101, dx01);
    MLERP::lerp(fx, m010, m110, dx10);
    MLERP::lerp(fx, m011, m111, dx11);
    MLERP::lerp(fy, dx00, dx10, dxy0);
    MLERP::lerp(fy, dx01, dx11, dxy1);
    MLERP::lerp(fz, dxy0, dxy1, mask);
    return mask;
  }

  RealType GetMaskAndGradient(RealType *mask_gradient)
  {
    // Interpolate the mask
    RealType dx00, dx01, dx10, dx11, dxy0, dxy1, mask;
    MLERP::lerp(fx, m000, m100, dx00);
    MLERP::lerp(fx, m001, m101, dx01);
    MLERP::lerp(fx, m010, m110, dx10);
    MLERP::lerp(fx, m011, m111, dx11);
    MLERP::lerp(fy, dx00, dx10, dxy0);
    MLERP::lerp(fy, dx01, dx11, dxy1);
    MLERP::lerp(fz, dxy0, dxy1, mask);

    // Compute the gradient of the mask
    RealType dx00_x, dx01_x, dx10_x, dx11_x, dxy0_x, dxy1_x;
    dx00_x = m100 - m000;
    dx01_x = m101 - m001;
    dx10_x = m110 - m010;
    dx11_x = m111 - m011;
    MLERP::lerp(fy, dx00_x, dx10_x, dxy0_x);
    MLERP::lerp(fy, dx01_x, dx11_x, dxy1_x);
    MLERP::lerp(fz, dxy0_x, dxy1_x, mask_gradient[0]);

    RealType dxy0_y, dxy1_y;
    dxy0_y = dx10 - dx00;
    dxy1_y = dx11 - dx01;    
    MLERP::lerp(fz, dxy0_y, dxy1_y, mask_gradient[1]);

    mask_gradient[2] = dxy1 - dxy0;

    return mask;
  }

protected:

  inline const InputComponentType *border_check(int X, int Y, int Z, RealType &mask)
  {
    if(X >= 0 && X < xsize && Y >= 0 && Y < ysize && Z >= 0 && Z < zsize)
      {
      mask = this->mask_buffer ? *(mens(X,Y,Z)) : 1.0;
      return dens(X,Y,Z);
      }
    else
      {
      mask = 0.0;
      return this->def_value;
      }
   }

  inline const InputComponentType *dens(int X, int Y, int Z)
  {
    return this->buffer + this->nComp * (X+xsize*(Y+ysize*Z));
  }

  inline const MaskPixelType *mens(int X, int Y, int Z)
  {
    return this->mask_buffer + X+xsize*(Y+ysize*Z);
  }

  // Image size
  int xsize, ysize, zsize;

  // Offsets
  int off_x, off_y, off_z;
  int off_mx, off_my, off_mz;

  // Image index
  int xind, yind, zind;

  // State of current interpolation
  const InputComponentType *d000, *d001, *d010, *d011, *d100, *d101, *d110, *d111;
  RealType m000, m001, m010, m011, m100, m101, m110, m111;

  RealType fx, fy, fz;
  int	 x0, y0, z0, x1, y1, z1;

};



/**
 * 2D fast linear interpolator - optimized for speed
 */
template <class TImage, class TFloat, class TMaskImage>
class FastLinearInterpolator<TImage, TFloat, 2, TMaskImage>
    : public FastLinearInterpolatorBase<TImage, TFloat, 2, TMaskImage>
{
public:
  typedef TImage                                                           ImageType;
  typedef TMaskImage                                                       MaskImageType;
  typedef FastLinearInterpolatorBase<ImageType, TFloat, 2, MaskImageType>  Superclass;
  typedef typename Superclass::InputComponentType                          InputComponentType;
  typedef typename Superclass::OutputComponentType                         OutputComponentType;
  typedef typename Superclass::RealType                                    RealType;
  typedef typename Superclass::InOut                                       InOut;
  typedef typename Superclass::MaskPixelType                               MaskPixelType;
  typedef typename Superclass::RegionType                                  RegionType;
  typedef LinearInterpolateImpl<OutputComponentType, RealType>             LERP;
  typedef LinearInterpolateImpl<RealType, RealType>                        MLERP;


  FastLinearInterpolator(ImageType *image, const RegionType &region, MaskImageType *mask = nullptr) : Superclass(image, region, mask)
  {
    xind = region.GetIndex()[0];
    yind = region.GetIndex()[1];

    xsize = region.GetSize()[0];
    ysize = region.GetSize()[1];

    off_x = this->nComp;
    off_y = xsize * off_x;
  }

  FastLinearInterpolator(ImageType *image, MaskImageType *mask = NULL) : FastLinearInterpolator(image, image->GetLargestPossibleRegion(), mask) {}

  /**
   * Compute the pointers to the eight corners of the interpolating cube
   */
  InOut ComputeCorners(RealType *cix)
  {
    RealType fl_cx = floor(cix[0]);
    RealType fl_cy = floor(cix[1]);
    fx = cix[0] - fl_cx;
    fy = cix[1] - fl_cy;
    x0 = ((int) fl_cx) - xind;
    y0 = ((int) fl_cy) - yind;
    x1 = x0 + 1;
    y1 = y0 + 1;

    if (x0 >= 0 && x1 < xsize &&
        y0 >= 0 && y1 < ysize)
      {
      // The sample point is completely inside
      d00 = dens(x0, y0);
      d10 = d00 + off_x;
      d01 = d00 + off_y;
      d11 = d01 + off_x;

      // Is there a mask? If so, sample the mask
      if(this->mask_buffer)
        {
        // Sample the mask
        const MaskPixelType *mp = mens(x0, y0);
        m00 = *mp;
        m10 = *(mp+1);
        mp += xsize;
        m01 = *mp;
        m11 = *(mp+1);

        // Check the mask - if != 1 for any pixel, this is considered a border pixel
        if(m00 == 1 && m01 == 1 && m10 == 1 && m11 == 1)
          {
          this->status = Superclass::INSIDE;
          }
        else if (m00 == 0 && m01 == 0 && m10 == 0 && m11 == 0)
          {
          this->status = Superclass::OUTSIDE;
          }
        else
          {
          this->status = Superclass::BORDER;
          }
        }
      else
        {
        // The mask is one
        this->status = Superclass::INSIDE;
        }
      }
    else if (x0 >= -1 && x1 <= xsize &&
             y0 >= -1 && y1 <= ysize)
      {
      // The sample point is on the border region
      d00 = border_check(x0, y0, m00);
      d01 = border_check(x0, y1, m01);
      d10 = border_check(x1, y0, m10);
      d11 = border_check(x1, y1, m11);

      // The mask is between 0 and 1
      if(this->mask_buffer &&
         (m00 == 0 && m01 == 0 && m10 == 0 && m11 == 0))
        this->status = Superclass::OUTSIDE;
      else
        this->status = Superclass::BORDER;
      }
    else
      {
      // The mask is zero
      this->status = Superclass::OUTSIDE;
      }

    return this->status;
  }

  void GetIndexAndRemainer(int *index, RealType *remainder)
  {
    index[0] = this->x0; index[1] = this->y0;
    remainder[0] = this->fx; remainder[1] = this->fy;
  }

  /**
   * Interpolate at position cix, placing the intensity values in out and gradient
   * values in grad (in strides of VDim)
   */
  InOut InterpolateWithGradient(RealType *cix, OutputComponentType *out, OutputComponentType **grad)
  {
    OutputComponentType dx0, dx1;

    // Compute the corners
    this->ComputeCorners(cix);

    if(this->status != Superclass::OUTSIDE)
      {
      // Loop over the components
      for(int iComp = 0; iComp < this->nComp; iComp++, grad++,
          d00++, d01++, d10++, d11++)
        {
        // Interpolate the image intensity
        LERP::lerp(fx, *d00, *d10, dx0);
        LERP::lerp(fx, *d01, *d11, dx1);
        LERP::lerp(fy, dx0, dx1, *(out++));

        // Interpolate the gradient in x
        LERP::lerp(fy, *d10 - *d00, *d11 - *d01, (*grad)[0]);

        // Interpolate the gradient in y
        (*grad)[1] = dx1 - dx0;
        }
      }

    return this->status;
  }

  InOut Interpolate(RealType *cix, OutputComponentType *out)
  {
    OutputComponentType dx0, dx1;

    // Compute the corners
    this->ComputeCorners(cix);

    if(this->status != Superclass::OUTSIDE)
      {
      // Loop over the components
      for(int iComp = 0; iComp < this->nComp; iComp++,
          d00++, d01++, d10++, d11++)
        {
        // Interpolate the image intensity
        LERP::lerp(fx, *d00, *d10, dx0);
        LERP::lerp(fx, *d01, *d11, dx1);
        LERP::lerp(fy, dx0, dx1, *(out++));
        }
      }

    return this->status;
  }

  InOut InterpolateNearestNeighbor(RealType *cix, OutputComponentType *out)
  {
    RealType px = cix[0] - xind, py = cix[1] - yind;
    x0 = (int) floor(px + 0.5);
    y0 = (int) floor(py + 0.5);

    if (x0 >= 0 && x0 < xsize && y0 >= 0 && y0 < ysize)
      {
      const InputComponentType *dp = dens(x0, y0);
      for(int iComp = 0; iComp < this->nComp; iComp++)
        {
        out[iComp] = dp[iComp];
        }
      return Superclass::INSIDE;
      }
    else return Superclass::OUTSIDE;
  }

  InOut Splat(RealType *cix, const InputComponentType *value)
  {
    // Compute the corners
    this->ComputeCorners(cix);

    // When inside, no checks are required
    if(this->status != Superclass::OUTSIDE)
      {
      // Compute the corner weights using 4 multiplications (not 16)
      RealType fxy = fx * fy;

      RealType w11 = fxy;
      RealType w01 = fy - fxy;
      RealType w10 = fx - fxy;
      RealType w00 = 1.0 - fx - fy + fxy;

      // Loop over the components
      if(this->status == Superclass::INSIDE)
        {
        for(int iComp = 0; iComp < this->nComp; iComp++,
            d00++, d01++, d10++, d11++, value++)
          {
          // Assign the appropriate weight to each part of the histogram
          InputComponentType val = *value;

          *const_cast<InputComponentType *>(d00) += w00 * val;
          *const_cast<InputComponentType *>(d01) += w01 * val;
          *const_cast<InputComponentType *>(d10) += w10 * val;
          *const_cast<InputComponentType *>(d11) += w11 * val;
          }
        }
      else
        {
        auto *dv = this->def_value;
        for(int iComp = 0; iComp < this->nComp; iComp++,
            d00++, d01++, d10++, d11++, value++, ++dv)
          {
          // Assign the appropriate weight to each part of the histogram
          InputComponentType val = *value;

          if(d00 != dv) *const_cast<InputComponentType *>(d00) += w00 * val;
          if(d01 != dv) *const_cast<InputComponentType *>(d01) += w01 * val;
          if(d10 != dv) *const_cast<InputComponentType *>(d10) += w10 * val;
          if(d11 != dv) *const_cast<InputComponentType *>(d11) += w11 * val;
          }
        }
      }

    return this->status;
  }

  template <class THistContainer>
  void PartialVolumeHistogramSample(RealType *cix, const InputComponentType *fixptr, THistContainer &hist)
  {
    // Compute the corners
    this->ComputeCorners(cix);

    if(this->status != Superclass::OUTSIDE)
      {
      // Compute the corner weights using 4 multiplications (not 16)
      RealType fxy = fx * fy;

      RealType w11 = fxy;
      RealType w01 = fy - fxy;
      RealType w10 = fx - fxy;
      RealType w00 = 1.0 - fx - fy + fxy;

      // Loop over the components
      for(int iComp = 0; iComp < this->nComp; iComp++,
          d00++, d01++, d10++, d11++, fixptr++)
        {
        // Just this line in the histogram
        RealType *hist_line = hist[iComp][*fixptr];

        // Assign the appropriate weight to each part of the histogram
        hist_line[*d00] += w00;
        hist_line[*d01] += w01;
        hist_line[*d10] += w10;
        hist_line[*d11] += w11;
        }
      }
    else
      {
      for(int iComp = 0; iComp < this->nComp; iComp++, fixptr++)
        {
        // Just this line in the histogram
        RealType *hist_line = hist[iComp][*fixptr];
        hist_line[0] += 1.0;
        }
      }
  }

  template <class THistContainer>
  void PartialVolumeHistogramGradientSample(RealType *cix, const InputComponentType *fixptr, const THistContainer &hist_w, RealType *out_grad)
  {
    // Compute the corners
    this->ComputeCorners(cix);

    // Outside values do not contribute to the gradient
    if(this->status != Superclass::OUTSIDE)
      {
      // Some horrendous derivatives here! Wow!
      RealType w11x = fy,               w11y = fx;
      RealType w01x = -fy,              w01y = 1 - fx;
      RealType w10x = 1 - fy,           w10y = -fx;
      RealType w00x = fy - 1,           w00y = fx - 1;

      // Initialize gradient to zero
      out_grad[0] = 0.0;
      out_grad[1] = 0.0;

      // Loop over the components
      for(int iComp = 0; iComp < this->nComp; iComp++,
          d00++, d01++, d10++, d11++, fixptr++)
        {
        // Just this line in the histogram
        const RealType *f = hist_w[iComp][*fixptr];

        // Take the weighted sum
        RealType f00 = f[*d00], f01 = f[*d01];
        RealType f10 = f[*d10], f11 = f[*d11];

        out_grad[0] += w00x * f00 + w01x * f01 + w10x * f10 + w11x * f11;
        out_grad[1] += w00y * f00 + w01y * f01 + w10y * f10 + w11y * f11;
        }
      }
    else
      {
      out_grad[0] = 0.0;
      out_grad[1] = 0.0;
      }
  }

  RealType GetMask()
  {
    // Interpolate the mask
    RealType dx0, dx1, mask;
    MLERP::lerp(fx, m00, m10, dx0);
    MLERP::lerp(fx, m01, m11, dx1);
    MLERP::lerp(fy, dx0, dx1, mask);
    return mask;
  }

  RealType GetMaskAndGradient(RealType *mask_gradient)
  {
    // Interpolate the mask
    RealType dx0, dx1, mask;
    MLERP::lerp(fx, m00, m10, dx0);
    MLERP::lerp(fx, m01, m11, dx1);
    MLERP::lerp(fy, dx0, dx1, mask);

    // Compute the gradient of the mask
    MLERP::lerp(fy, m10 - m00, m11 - m01, mask_gradient[0]);
    mask_gradient[1] = dx1 - dx0;

    return mask;
  }

protected:

  inline const InputComponentType *border_check(int X, int Y, RealType &mask)
  {
    if(X >= 0 && X < xsize && Y >= 0 && Y < ysize)
      {
      mask = this->mask_buffer ? *(mens(X,Y)) : 1.0;
      return dens(X,Y);
      }
    else
      {
      mask = 0.0;
      return this->def_value;
      }
   }

  inline const InputComponentType *dens(int X, int Y)
  {
    return this->buffer + this->nComp * (X+xsize*Y);
  }

  inline const MaskPixelType *mens(int X, int Y)
  {
    return this->mask_buffer + X+xsize*Y;
  }

  // Image size
  int xsize, ysize, xind, yind;
  int off_x, off_y;

  // State of current interpolation
  const InputComponentType *d00, *d01, *d10, *d11;
  RealType m00, m01, m10, m11;

  RealType fx, fy;
  int	 x0, y0, x1, y1;
};


#endif
