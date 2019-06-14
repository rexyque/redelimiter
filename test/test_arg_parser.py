import unittest, getopt
from redelimiter.arg_parser import *

class TestArgParser(unittest.TestCase):
    
    def test_get_args(self):
        valid_values = { 
            "-h": 
                ArgSet(h=True),
            "-i , -O | -- file.txt": 
                ArgSet(infiles=["file.txt"], indelim=',', outdelim='|'),
            "--outfile=file.tsv -- file.data": 
                ArgSet(infiles=["file.data"], outfile="file.tsv"),
            "-o multiple_files.tsv -- first_file.csv second_file.csv":
                ArgSet(infiles=["first_file.csv", "second_file.csv"], outfile="multiple_files.tsv"),
            "test_file.csv": # it's not get_args' job to know this is missing required args
                ArgSet(infiles=["test_file.csv"]),
            "-o output.tsv": # again, it's not get_args' job to know this is missing required args
                ArgSet(outfile="output.tsv")
        }

        invalid_values = ["-h -j", "-O", "-v --outfile=output.csv -- input.tsv"]

        for value, expected in valid_values.items():
            actual = get_args(value.split())
            with self.subTest(value=value):
                self.assertEqual(expected, actual)

        for value in invalid_values:
            with self.assertRaises(getopt.GetoptError):
                result = get_args(value.split())
                print(result)

class TestArgSet(unittest.TestCase):
    def test_fill_missing(self):
        valid_values = [
            (ArgSet(h=True), 
                ArgSet(h=True)),
            (ArgSet(infiles=["file.txt"], outfile="output.csv"),
                ArgSet(infiles=["file.txt"], indelim='|', outfile="output.csv", outdelim=',')),
            (ArgSet(infiles=["file.txt"], outdelim=','),
                ArgSet(infiles=["file.txt"], indelim='|', outfile="file.csv", outdelim=','))
        ]

        for actual, expected in valid_values:
            actual.fill_missing()
            self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
