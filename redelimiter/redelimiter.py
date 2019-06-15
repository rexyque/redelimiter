import csv

def redelimit(args):
    """Redelimits files based on the arguments passed to it"""
    with open(args.outfile, 'w', newline='') as outfile:
        for name in args.infiles:
            with open(name, newline='') as infile:
                convert_stream(infile, args.indelim, outfile, args.outdelim)

def convert_stream(instream, indelim, outstream, outdelim):
    """Converts the delimiter of a stream"""
    records = []
    reader = csv.reader(instream, delimiter=indelim)
    for row in reader:
        records.append(row)
    writer = csv.writer(outstream, delimiter=outdelim)
    writer.writerows(records)
