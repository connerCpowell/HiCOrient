__author__ = 'malonge'
import os
import unittest

from hic_orientation.SeqReader import SeqReader


class SeqReaderTest(unittest.TestCase):

    def setUp(self):
        # Make a fasta file that adheres to fasta convention.
        # Alternate header and sequence each line.
        with open('good_alt_line.fasta', 'w') as f:
            # Write two lines of a fasta file
            f.write('>test1\n')
            f.write('AAAAAAAAAA\n')
            f.write('>test2\n')
            f.write('GGGGGGGGGG')

        # Make a fasta file that adheres to fasta convention.
        # Do not alternate header and sequence each line.
        with open('good_non_alt_line.fasta', 'w') as f:
            # Write two lines of a fasta file
            f.write('>test1\n')
            f.write('AAAAA\n')
            f.write('AAAAA\n')
            f.write('>test2\n')
            f.write('GGGGG\n')
            f.write('GGGGG\n')

        # Make a fasta file that does not adhere to fasta convention
        # first line is a comment.
        with open('bad_comment.fasta', 'w') as f:
            # Write two lines of a fasta file
            f.write('#This is a comment\n')
            f.write('>test\n')
            f.write('AAAAAAAAAA\n')
            f.write('>test\n')
            f.write('GGGGGGGGGG')

        # Make a fasta file that does not adhere to fasta convention
        # No headers.
        with open('bad_no_header.fasta', 'w') as f:
            # Write two lines of a fasta file
            f.write('AAAAAAAAAA\n')
            f.write('GGGGGGGGGG')

        # Make a fasta file that has two headers per one sequence
        with open('two_headers.fasta', 'w') as f:
            f.write('>test1\n')
            f.write('>test1_again\n')
            f.write('AAAAAAAAAA\n')
            f.write('>test2\n')
            f.write('>test2_again\n')
            f.write('GGGGGGGGGG')

        # Make a fastq file that adheres to fastq convention
        with open('good.fastq', 'w') as f:
            f.write('@header\n')
            f.write('AAAAAAAAAA\n')
            f.write('+\n')
            f.write('QQQQQQQQQQ\n')

        # Make a fastq file where the number of lines is not a multiple of 4.
        with open('bad_line_number.fastq', 'w') as f:
            f.write('@header\n')
            f.write('AAAAAAAAAA\n')
            f.write('+\n')
            f.write('QQQQQQQQQQ\n')
            f.write('@header')

    def tearDown(self):
        os.remove('good_alt_line.fasta')
        os.remove('good_non_alt_line.fasta')
        os.remove('bad_comment.fasta')
        os.remove('bad_no_header.fasta')
        os.remove('good.fastq')
        os.remove('bad_line_number.fastq')
        os.remove('two_headers.fasta')

    def test_init_one(self):
        with self.assertRaises(AttributeError):
            x = SeqReader(True)

    def test_non_existent_file(self):
        with self.assertRaises(IOError):
            x = SeqReader('fake_file_that_does_not_exists.fasta')
            for header, sequence in x.parse_fasta():
                pass

    def test_good_alt_lines_fasta(self):
        x = SeqReader('good_alt_line.fasta')
        fasta_iter = x.parse_fasta()

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test1')
        self.assertEqual(sequence, 'AAAAAAAAAA')

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test2')
        self.assertEqual(sequence, 'GGGGGGGGGG')

    def test_good_non_alt_lines_fasta(self):
        x = SeqReader('good_non_alt_line.fasta')
        fasta_iter = x.parse_fasta()

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test1')
        self.assertEqual(sequence, 'AAAAAAAAAA')

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test2')
        self.assertEqual(sequence, 'GGGGGGGGGG')

    def test_bad_comment(self):
        x = SeqReader('bad_comment.fasta')
        fasta_iter = x.parse_fasta()

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test')
        self.assertEqual(sequence, 'AAAAAAAAAA')

        header, sequence = fasta_iter.next()
        self.assertEqual(header, '>test')
        self.assertEqual(sequence, 'GGGGGGGGGG')

    def test_no_header(self):
        with self.assertRaises(RuntimeError):
            x = SeqReader('bad_no_header.fasta')
            for header, seq in x.parse_fasta():
                pass

if __name__ == '__main__':
    unittest.main()