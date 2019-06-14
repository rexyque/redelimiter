import csv

def convert_stream(instream, indelim, outstream, outdelim):
    records = []
    dialect = csv.Sniffer().sniff(instream.read(1024))
    dialect.skipinitialspace = False
    instream.seek(0)
    reader = csv.reader(instream, dialect, delimiter=indelim)
    for row in reader:
        records.append(row)
    writer = csv.writer(outstream, dialect, delimiter=outdelim)
    writer.writerows(records)
