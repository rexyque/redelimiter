import io
import unittest
import redelimiter.redelimiter as rede

class TestRedelimiter(unittest.TestCase):

    def test_convert_stream(self):
        values = {
                (',', 'Hello, World!'):
                    ('|', 'Hello| World!\r\n'),
                (',', 'This,csv,has\nthree,rows,and\nthree,columns,too'):
                    ('\t', 'This\tcsv\thas\r\nthree\trows\tand\r\nthree\tcolumns\ttoo\r\n'),
                (',', 'Here we have,to use a qualifier\n"because, well, it\'s",necessary sometimes'):
                    ('|', 'Here we have|to use a qualifier\r\nbecause, well, it\'s|necessary sometimes\r\n'),
                ('\t', 'This one\twill need\na qualifier, inside\tthe output.'):
                    (',', 'This one,will need\r\n"a qualifier, inside",the output.\r\n'),
                (',', 'The|qualifier in,this one\n"will, have to",move!'):
                    ('|', '"The|qualifier in"|this one\r\nwill, have to|move!\r\n')
                }
        for value, expected in values.items():
            instream = io.StringIO(initial_value=value[1], newline='')
            outstream = io.StringIO(newline='')
            rede.convert_stream(instream, value[0], outstream, expected[0])
            actual = outstream.getvalue()
            with self.subTest(value=value, expected=expected, actual=actual):
                self.assertEqual(expected[1], actual)

if __name__ == '__main__':
    unittest.main()
