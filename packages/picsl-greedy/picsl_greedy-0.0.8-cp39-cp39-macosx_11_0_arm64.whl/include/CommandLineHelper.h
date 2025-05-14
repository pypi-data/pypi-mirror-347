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
#ifndef COMMANDLINEHELPER_H
#define COMMANDLINEHELPER_H

#include <cerrno>
#include "GreedyException.h"
#include "GreedyParameters.h"
#include "itksys/SystemTools.hxx"

char **split_commandline(const char *cmdline, int *argc);

/**
 * @brief A class to facilitate processing of command-line arguments
 */
class CommandLineHelper
{
public:
  CommandLineHelper(int argc, char *argv[])
  {
    this->argc = argc;
    this->argv = argv;
    this->i = 1;
    this->own_argv = false;
  }

  CommandLineHelper(const char *cmdl)
  {
    this->argc = 0;
    this->argv = split_commandline(cmdl, &argc);
    this->i = 0;
    this->own_argv = true;
  }

  ~CommandLineHelper()
  {
    if(this->own_argv && this->argv)
      for (i = 0; i < this->argc; i++)
        if (this->argv[i])
          free(this->argv[i]);
  }

  /**
   * Set the data root directory. All filenames will be read relative to this
   */
  void set_data_root(const char *root = nullptr)
  {
    if(root)
      data_root = root;
    else
      data_root = std::string();
  }

  /**
   * Provide a set of strings that should be accepted as existing filenames if
   * encountered. This is to allow in-memory objects to be presented as filename
   * inputs to the program
   */
  void set_file_check_bypass_labels(std::vector<std::string> labels)
  {
    this->file_check_bypass_labels = labels;
  }

  bool is_at_end()
  {
    return i >= argc;
  }

  /**
   * Just read the next arg (used internally)
   */
  const char *read_arg()
  {
    if(i >= argc)
      throw GreedyException("Unexpected end of command line arguments.");

    return argv[i++];
  }

  /**
   * Peek at the next argument, without treating it as 'read'. Useful when arguments
   * of different type are possible
   */
  const char *peek_arg()
  {
    if(i >= argc)
      throw GreedyException("Unexpected end of command line arguments.");
    return argv[i];
  }

  /**
   * Read a command (something that starts with a '-')
   */
  std::string read_command()
  {
    current_command = read_arg();
    if(current_command[0] != '-')
      throw GreedyException("Expected a command at position %d, instead got '%s'.", i, current_command.c_str());
    return current_command;
  }

  /**
   * Read a command if available (there are arguments remaining)
   */
  bool read_command(std::string &cmd)
  {
    if(i >= argc || peek_arg()[0] != '-')
      return false;
    cmd = read_command();
    return true;
  }

  /**
   * Read a string that is not a command (may not start with a -)
   */
  std::string read_string()
  {
    std::string arg = read_arg();
    if(arg[0] == '-')
      throw GreedyException("Expected a string argument as parameter to '%s', instead got '%s'.", current_command.c_str(), arg.c_str());

    return arg;
  }


  /**
   * Get the number of free arguments to the current command. Use only for commands with
   * a priori unknown number of arguments. Otherwise, just use the get_ commands
   */
  int command_arg_count(int min_required = 0)
  {
    // Count the number of arguments
    int n_args = 0;
    for(int j = i; j < argc; j++, n_args++)
      if(argv[j][0] == '-')
        break;

    // Test for minimum required
    if(n_args < min_required)
      throw GreedyException(
          "Expected at least %d arguments to '%s', instead got '%d'",
          min_required, current_command.c_str(), n_args);

    return n_args;
  }

  bool is_file_check_bypass_label(const std::string &s)
  {
    return std::find(file_check_bypass_labels.begin(), file_check_bypass_labels.end(), s) != file_check_bypass_labels.end();
  }

  /**
   * Read an existing filename
   */
  std::string read_existing_filename()
  {
    std::string file = read_arg();
    if(is_file_check_bypass_label(file))
      return file;

    if(this->data_root.length())
      file = itksys::SystemTools::CollapseFullPath(file, data_root);

    if(!itksys::SystemTools::FileExists(file.c_str()))
      throw GreedyException("File '%s' does not exist", file.c_str());

    return file;
  }

  /**
   * Read a transform specification, format file,number
   */
  TransformSpec read_transform_spec(bool check_file_exists = true)
  {
    std::string spec = read_arg();
    size_t pos = spec.find_first_of(',');

    TransformSpec ts;
    ts.filename = spec.substr(0, pos);
    ts.exponent = 1.0;


    if(this->data_root.length())
      ts.filename = itksys::SystemTools::CollapseFullPath(ts.filename, data_root);

    if(!is_file_check_bypass_label(ts.filename.c_str()))
      if(check_file_exists && !itksys::SystemTools::FileExists(ts.filename.c_str()))
        throw GreedyException("File '%s' does not exist", ts.filename.c_str());

    if(pos != std::string::npos)
      {
      errno = 0; char *pend;
      std::string expstr = spec.substr(pos+1);
      ts.exponent = std::strtod(expstr.c_str(), &pend);

      if(errno || *pend)
        throw GreedyException("Expected a floating point number after comma in transform specification '%s', instead got '%s'",
                              current_command.c_str(), spec.substr(pos).c_str());

      }

    return ts;
  }

  /**
   * Read an output filename
   */
  std::string read_output_filename()
  {
    std::string file = read_arg();
    if(is_file_check_bypass_label(file))
      return file;
    if(this->data_root.length())
      file = itksys::SystemTools::CollapseFullPath(file, data_root);
    return file;
  }

  /**
   * Read a floating point value
   */
  double read_double()
  {
    std::string arg = read_arg();

    errno = 0; char *pend;
    double val = std::strtod(arg.c_str(), &pend);

    if(errno || *pend)
      throw GreedyException("Expected a floating point number as parameter to '%s', instead got '%s'",
                            current_command.c_str(), arg.c_str());

    return val;
  }

  /**
   * Read output directory path
   */
  std::string read_output_dir()
  {
    std::string dir = read_arg();
    if(this->data_root.length())
      dir = itksys::SystemTools::CollapseFullPath(dir, data_root);

    if(!itksys::SystemTools::PathExists(dir.c_str()))
      throw GreedyException("Folder '%s' does not exist", dir.c_str());

    return dir;
  }

  /**
   * Check if a string ends with another string and return the
   * substring without the suffix
   */
  bool check_suffix(const std::string &source, const std::string &suffix, std::string &out_prefix)
  {
    int n = source.length(), m = suffix.length();
    if(n < m)
      return false;

    if(source.substr(n-m, m) != suffix)
      return false;

    out_prefix = source.substr(0, n-m);
    return true;
  }

  /**
   * Read a floating point value with units (mm or vox)
   */
  double read_scalar_with_units(bool &physical_units)
  {
    std::string arg = read_arg();
    std::string scalar;

    if(check_suffix(arg, "vox", scalar))
      physical_units = false;
    else if(check_suffix(arg, "mm", scalar))
      physical_units = true;
    else
      throw GreedyException("Parameter to '%s' should include units, e.g. '3vox' or '3mm', instead got '%s'",
                            current_command.c_str(), arg.c_str());

    errno = 0; char *pend;
    double val = std::strtod(scalar.c_str(), &pend);

    if(errno || *pend)
      throw GreedyException("Expected a floating point number as parameter to '%s', instead got '%s'",
                            current_command.c_str(), scalar.c_str());

    return val;
  }

  /**
   * Read an integer value
   */
  long read_integer()
  {
    std::string arg = read_arg();

    errno = 0; char *pend;
    long val = std::strtol(arg.c_str(), &pend, 10);

    if(errno || *pend)
      throw GreedyException("Expected an integer as parameter to '%s', instead got '%s'",
                            current_command.c_str(), arg.c_str());

    return val;
  }

  /**
   * Read one of a list of strings. The optional parameters to this are in the form
   * int, string, int, string, int, string. Each string may in turn contain a list
   * of words (separated by space) that are acceptable. So for example. NULL string
   * is used to refer to the default option.
   *
   * enum Mode { NORMAL, BAD, SILLY }
   * Mode m = X.read_option(NORMAL, "NORMAL normal", BAD, "bad BAD", SILLY, NULL);
   */
  /*
  template <class TOption>
  TOption read_option(TOption opt1, const char *str1, ...)
  {
    not implemented yet
  }
  */

  /**
   * Read a vector in the format 1.0x0.2x0.6
   */
  std::vector<double> read_double_vector()
  {
    std::string arg = read_arg();
    std::istringstream f(arg);
    std::string s;
    std::vector<double> vector;
    while (getline(f, s, 'x'))
      {
      errno = 0; char *pend;
      double val = std::strtod(s.c_str(), &pend);

      if(errno || *pend)
        throw GreedyException("Expected a floating point vector as parameter to '%s', instead got '%s'",
                              current_command.c_str(), arg.c_str());
      vector.push_back(val);
      }

    if(!vector.size())
      throw GreedyException("Expected a floating point vector as parameter to '%s', instead got '%s'",
                            current_command.c_str(), arg.c_str());

    return vector;
  }

  std::vector<int> read_int_vector(char delimiter = 'x')
  {
    std::string arg = read_arg();
    std::istringstream f(arg);
    std::string s;
    std::vector<int> vector;
    while (getline(f, s, delimiter))
      {
      errno = 0; char *pend;
      long val = std::strtol(s.c_str(), &pend, 10);

      if(errno || *pend)
        throw GreedyException("Expected an integer vector delimited by '%c' as parameter to '%s', instead got '%s'",
                              delimiter, current_command.c_str(), arg.c_str());
      vector.push_back((int) val);
      }

    if(!vector.size())
      throw GreedyException("Expected an integer vector delimited by '%c' as parameter to '%s', instead got '%s'",
                            delimiter, current_command.c_str(), arg.c_str());
    return vector;
  }

  /** Remove the last k commands from the parser, and return a new parser for those commands */
  CommandLineHelper take_end(int k)
  {
    if(k > argc)
      throw GreedyException("Cannot take last %d commands from commandline", k);

    argc -= k;
    return CommandLineHelper(k, argv + argc);
  }

private:
  int argc, i;
  char **argv;
  bool own_argv;
  std::string current_command;
  std::string data_root;
  std::vector<std::string> file_check_bypass_labels;
};

/** Helper function to expand a command line string to argc/argv format */
char **split_commandline(const char *cmdline, int *argc);
void free_argv(int argc, char **argv);

#endif // COMMANDLINEHELPER_H
