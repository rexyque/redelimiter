#!/usr/bin/env python

"""A simple command line utility for converting the delimiter of delimited files.

Usage:
    redelimit [options] (--outfile=<filename>|--outdelim=<char>)... -- <infile>...
    redelimit -h

Options:
    REQUIRED

    infile                      Name of the file or files to process.
    -o, --outfile=<filename>    Name of the file to output to. If not specified, defaults 
                                    to the name of the infile with the extension changed to 
                                    the default extension for the delimiter. If that is
                                    the same extension, "_out" will be appended to the
                                    filename before the extension.
    -O, --outdelim=<char>       Single character delimiter for output. If not specified,
                                    defaults to the default delimiter for the extension of
                                    outfile.
    Only one of either outfile or outdelim is required. They can both be specified.

    OPTIONAL

    -h, --help                  Show this help message and exit.
    -i, --indelim=<char>        The delimiter to use when processing infile. If not
                                    specified, defaults to the default delimiter for the
                                    extension of the first infile.
    
Defaults:
    EXTENSION   DELIMITER
    .csv        ','
    .tsv        '\\t'
    .txt        '|'

    The default delimiter for other file types is ',' and the default extension
    for other delimiters is .txt
"""

import sys
from arg_parser import *
from redelimiter import *

def main():
    args = parse_args(sys.argv[1:])
    if args.help:
        print(__doc__)
        sys.exit(0)
    redelimit(args)

if __name__ == "__main__":
    main()
