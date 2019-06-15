import getopt, sys

def get_default_ext(delim):
    """Retrieves the default extension for a delimiter"""
    if delim == ',':
        return "csv"
    if delim == '\t':
        return "tsv"
    return "txt"

def get_default_delim(ext):
    """Retrieves the default delimiter for a file extension"""
    if ext == "tsv":
        return '\t'
    if ext == "txt":
        return '|'
    return ','

class ArgSet:
    """The set of arguments for redelimiter to use"""
    def __init__(self, infiles=[], indelim=None, outfile=None, outdelim=None, h=False):
        self.infiles = infiles
        self.indelim = indelim
        self.outfile = outfile
        self.outdelim = outdelim
        self.help = h

    def __eq__(self, other):
        return self.infiles == other.infiles and \
               self.indelim == other.indelim and \
               self.outfile == other.outfile and \
               self.outdelim == other.outdelim and \
               self.help == other.help

    def __repr__(self):
        return 'ArgSet(infiles={}, indelim={}, outfile={}, outdelim={}, h={})'.format(
                self.infiles, self.indelim, self.outfile, self.outdelim, self.help)

    def __validate(self):
        """Validates the argument set. Will raise ArgumentError if it is not valid"""
        if len(self.infiles) == 0:
            raise ArgumentMissingError("infile")
        if self.outfile is None and self.outdelim is None:
            raise ArgumentMissingError("outfile or outdelim")
        if self.outdelim is not None and len(self.outdelim) != 1:
            raise ArgumentValueError("outdelim", self.outdelim)
        if self.indelim is not None and len(self.indelim) != 1:
            raise ArgumentValueError("indelim", self.indelim)

    def __fill_indelim(self):
        """Fills in indelim with the default value if it is None"""
        if self.indelim == None:
            name, ext = split_filename(self.infiles[0])
            self.indelim = get_default_delim(ext)

    def __fill_outdelim(self):
        """Fills in outdelim with the default value if it is None"""
        if self.outdelim == None:
            name, ext = split_filename(self.outfile)
            self.outdelim = get_default_delim(ext)

    def __fill_outfile(self):
        """Fills in outfile with the default value if it is None"""
        if self.outfile == None:
            name, ext = split_filename(self.infiles[0])
            outext = get_default_ext(self.outdelim)
            if ext == outext:
                name += "_out"
            self.outfile = name + '.' + outext

    def fill_missing(self):
        """Validates the argument set and fills in any missing optional arguments with their default values"""
        if not self.help:
            self.__validate()
            self.__fill_indelim()
            self.__fill_outdelim()
            self.__fill_outfile()
            self.__fill_outdelim()

class ArgumentError(Exception):
    """Base class for errors with input arguments"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class ArgumentMissingError(ArgumentError):
    """Raised when a required argument is missing"""
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return "Missing required argument: {}".format(self.arg)

class ArgumentValueError(ArgumentError):
    """Raised when an argument has an invalid value"""
    def __init__(self, arg, val):
        self.arg = arg
        self.val = val

    def __str__(self):
        return "Invalid value for argument {}: {}".format(self.arg, self.val)

def split_filename(name):
    """Splits a string containing a file name into the filename and extension"""
    dot = name.rfind('.')
    if (dot == -1):
        return name, ''
    return name[:dot], name[dot + 1:]

def usage():
    """Prints a one line usage message"""
    print("run 'redelimit --help' to see usage")

def get_args(argv):
    """Extracts the arguments from argv. Raises GetoptError if there are unrecognized arguments"""
    opts, args = getopt.getopt(argv, "hi:o:O:", ["help", "indelim=", "outfile=", "outdelim="])
    result = ArgSet(infiles=[]) # the infiles=[] seems arbitrary, but for some reason
                                # the list doesn't get dropped when running tests, so
                                # the second test (and those after) with infiles
                                # will always fail
    for o, a in opts:
        if o in ("-h", "--help"):
            result.help = True
            return result
        elif o in ("-i", "--indelim"):
            result.indelim = a
        elif o in ("-o", "--outfile"):
            result.outfile = a
        elif o in ("-O", "--outdelim"):
            result.outdelim = a
        else:
            assert False, "unhandled option"
    for arg in args:
        result.infiles.append(arg)
    return result

def parse_args(argv):
    """Converts argv into the set of arguments to pass to redelimiter"""
    try:
        args = get_args(argv)
        args.fill_missing()
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)
    except ArgumentError as err:
        print(err)
        usage()
        sys.exit(2)
    return args
