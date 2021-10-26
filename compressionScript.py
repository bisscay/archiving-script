#!/usr/bin/python

# compressionScript.py
# Gzip compression of files in a directory into year-month archives 
# Author: Bissallah Ekele - bAe
# Date: 6/4/2021

# Copyright (C) 2021 Bissallah Ekele
# License GPLv3+: GNU GPL version 3 or later
# <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.

import os 
import zipfile
import time
import sys
import getopt
import datetime

# TODO: Convert block comments to docstrings

# usage()
# Trimmed help prompt
def usage():
    usage = """SYNOPSIS
compressionScript.py [-s | --sourceLocation] <source-location> [OPTION]\
 <option-argument>

Please see help for detailed usage.
i.e compressionScript.py -h
"""
    print(usage)

# help()
# Source directory is mandatory
# By default compression starts from April, 2021
# Months and years are one-base indexed; i.e January == 1
# Compression destination defaults to archive folder in source-directory
# @throws SystemExit, exit the interpreter with a success status
def help():
    help = """NAME
compressionScript.py - compress files in a directory to\
 year-month archives using Gzip.

SYNOPSIS
    ./compressionScript.py [-s | --sourceLocation] <source-location>\
 [OPTION]...

SYNTAX
    ./compressionScript.py [-s | --sourceLocation] <source-location> \\
    [-o | --outputLocation] <output-location> [-m | -startMonth]\
 <start-month> \\
    [-y | -startYear] <start-year> --endMonth <end-month> --endYear\
 <end-year>
    
DESCRIPTION
    Gzip compression of files in a directory into Year-Month archives.

    Source directory is required, all other options are optional.

    By default compression starts from April, 2021.

    Compression destination defaults to an archive folder in the\
 source directory.

    Months and years are one-base indexed; i.e January == 1.

    End-year if specified must be greater or equal to start-year,
    else current-year is used.

    If end-year is equal, end-month must be equal or greater than\
 start-month,
    else current-month is used.

    Negative month(s) or year(s) are seen as invalid options.

    Month(s) over 12-th will default month value(s).

    Mandatory arguments to long options are mandatory to short options too.

    Options:
    -s, --sourceLocation=DIR
        directory to get files to be compressed

    -o, --outputLocation=DIR
        directory to place the archives categorized in year-month labels

    -m, --startMonth=MON
        files created from this start month are analysed.\
 Defaults to April; i.e 4

    -y, --startYear=YR
        files created from this start year are analysed. Defaults to 2021

    --endMonth=MON
        examines files from start-month to specified month.\
 Defaults to current month

    --endYear=YR
        considers files from start-year to specified year.\
 Defaults to current year.

EXIT STATUS:
0   if OK,

1   if cannot access directory,

2   if cannot access command-line argument.
"""
    print(help)

    sys.exit(0)

# get_bash_parse()
# Parse options and option-argument provided in CLI
# @return opts - list, option and option-argument tuples in a list 
def get_bash_parse():
    bash_arguments = sys.argv[1:]

    unix_options = "hs:o:m:y:"
    gnu_options = [
        "sourceLocation=",
        "outputLocation=",
        "startMonth=",
        "startYear=",
        "endMonth=",
        "endYear=",
        ]

    opts = None # Not necessary
    try:
        opts, _ = getopt.getopt(
            bash_arguments, unix_options, gnu_options)
    except getopt.GetoptError as e:
        usage()
        sys.stderr.write(repr(e))
        sys.exit(2)
    return opts

# TODO:
# validate_parse()
# End-year if specified must be greater or equal to start-year,
# else current-year is used
# If end-year is equal, end-month must be >= start-month,
# else current-month is used
# Negative month(s) or year(s) are seen as invalid options
# Month(s) over 12-th will default value(s) 
def validate_parse():
    pass

# compute_epoch()
# Compute the naive epoch for a give timestamp
# Year and month is sufficient for this use case
# @param year - int, timestamp-year
# @param month - int, timestamp-month
# @return float, POSIX timestamp in seconds
def compute_epoch(year, month):
    timedelta_object = (datetime.datetime(year, month, 1)
                        - datetime.datetime(1970, 1, 1))
    return (timedelta_object.microseconds
            + (timedelta_object.seconds + timedelta_object.days * 86400)
            * 10**6) / 10**6

# group_files()
# Group files into lists based on Year_Month keys
# M-Time is specified here, can be changed to C-Time
# @param parent_path - Path-like String, folder containing files
# @param zip_location - Path-like String, where to place the archive
# @param start_month - int, start-month-stamp, 1-based indexing
# @param start_year - int, start-year-stamp, 1-based indexing
# @param end_moth - int, end-month-stamp, 1-based indexing
# @param end_year - int, end-year-stamp, 1-based indexing
# @return hashmap - dict, file year-month grouping
def group_files(parent_path, zip_location, start_month, start_year,
                end_month, end_year):
    hashmap = {}
    post_end_month = end_month + 1
    try:
        for file_name in os.listdir(parent_path):
            if file_name == "archive":
                continue
            file_path = os.path.join(parent_path, file_name)
            epoch_time = os.path.getmtime(file_path) # M-Time
            local_time = time.localtime(epoch_time)
            start_range = compute_epoch(start_year, start_month)
            end_range = compute_epoch(end_year, post_end_month)
            if epoch_time >= start_range and epoch_time < end_range:
                archive_arguments = [
                    zip_location, "/",
                    str(local_time.tm_year), "_",
                    str(local_time.tm_mon), ".gz",
                    ]
                archive = "".join(archive_arguments)
                if archive not in hashmap:
                    hashmap[archive] = [file_name,]
                else:
                    hashmap[archive].append(file_name)
        return hashmap
    except ValueError as e:
        assert False, "ValueError: Check date-time arguments\n" + repr(e)
    except OSError as e:
        sys.exit(repr(e))

# compress_file()
# Compress files in parent path to an archive in zip location
# @param parent_path - String, directory containing files to compress
# @param zip_location - Path-like String, where to place the archive
# @param start_month - int, start month-stamp, 1-based indexing
# @param start_year - int, start-year-stamp, 1-based indexing
# @param end_moth - int, end-month-stamp, 1-based indexing
# @param end_year - int, end-year-stamp, 1-based indexing
def compress_file(parent_path, zip_location, start_month, start_year,
                    end_month, end_year):
    hashmap = group_files(parent_path, zip_location, start_month,
                            start_year, end_month, end_year)
    try:
        for archive in hashmap:
            zip_file_object = zipfile.ZipFile(
                archive, mode="a", compression=zipfile.ZIP_DEFLATED)
            try:
                for file_name in hashmap[archive]:
                    file_path = os.path.join(parent_path, file_name)
                    zip_file_object.write(file_path, file_name)
                    os.remove(file_path)
            finally:
                if zip_file_object:
                    zip_file_object.close()
    except OSError as e:
        sys.exit(repr(e))
    except NotImplementedError as e:
        assert False, "Check compression-argument." \
                        "\nMust be a recognized argument." + repr(e)
    except RuntimeError as e:
        # Run-time concatenation due to low chance of absent module
        sys.exit(
            ("zlib module is absent."
            + "\nGzip-algorithm requires zlib module."
            + "\nOptionally, try other algorithms:"
            + "\nDefault from ZIP_DEFLATED to ZIP_BZIP2 or ZIP_LMZA."
            + "\nNote: You will no longer be using gzip-algorithm"
            + " once changed!"
            + repr(e)))
    
# Driver Code
def main():
    parent_path = zip_location = None
    start_month = 4
    start_year = 2021
    current_time = time.localtime()
    end_month = current_time.tm_mon
    end_year = current_time.tm_year
    
    bash_parse = get_bash_parse()

    # Validate
    try:
        for o, a in bash_parse:
            if a in [
                "-s", "-o", "-m", "-y", "--sourceLocation",
                "--outputLocation", "--startMonth",
                "--startYear", "--endMonth", "--endYear",
                ]:
                raise ValueError(
                    ("ValueError: Check Option-argument(s),"
                    " must not be an Option(i.e flag or switch)."))
            
            if o == "-h":
                help()

            if o in ["-s", "--sourceLocation"]:
                parent_path = a
            elif o in ["-o", "--outputLocation"]:
                zip_location = a
            elif ((o in ["-m", "--startMonth"]) and a.isdigit() and
                int(a) >= 1 and int(a) <= 12):
                start_month = int(a)
            elif ((o in ["-y", "--startYear"]) and a.isdigit() and
                int(a) >= datetime.MINYEAR and int(a) <= datetime.MAXYEAR):
                start_year = int(a)
            elif ((o == "--endMonth") and a.isdigit() and
                int(a) >= 1 and int(a) <= 12):
                end_month = int(a)
            elif ((o == "--endYear") and a.isdigit() and
                int(a) >= datetime.MINYEAR and int(a) <= datetime.MAXYEAR):
                end_year = int(a)
            else:
                raise ValueError("Unhandled Option Parsed!")

        if end_year < start_year:
            end_year = current_time.tm_year
            end_month = current_time.tm_mon

        if end_year == start_year and end_month < start_month:
            end_month = current_time.tm_mon

        if not parent_path:
            raise ValueError("Source directory missing!")

        if not zip_location:
            zip_location = os.path.join(parent_path, "archive")
            try:
                os.mkdir(zip_location)
            except OSError as e:
                if os.strerror(e.errno) == "File exists":
                    pass
                else:
                    raise e

        compress_file(parent_path, zip_location, start_month,
                        start_year, end_month, end_year)
    except ValueError as e:
        usage()
        sys.stderr.write(str(e))
        sys.exit(2)
    except OSError as e:
        assert False, repr(e)

if __name__ == "__main__":
    main()