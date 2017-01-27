__author__ = 'malonge'


"""
Michael Alonge
SeqReader.py
Bare bones sequence file generator for fasta files.
e.g.
from SeqReader import SeqReader
x = SeqReader('sequences.fasta')
for header, sequence in x.parse_fasta():
    # Do stuff with header and sequence.
"""


class SeqReader:
    """
    Defines a generator method for fasta files. This method is bare bones,
    and simply yield the raw contents of the file provided.
    parse_fasta() --- fasta parser. Yields header, sequence for each sequence.
    """

    def __init__(self, in_file):
        """
        Initialize sequence file to be parsed.

        :param in_file: Fasta file
        """
        if not isinstance(in_file, str):
            raise AttributeError('Only a string can be used to instantiate a SeqReader object.')
        self.in_file = in_file

    def parse_fasta(self):
        """
        Generator yielding header and sequence, for each sequence
        in the fasta file sent to the class. Header and sequence are yielded as strings
        :return: Iterator of headers and sequences as strings.
        """
        with open(self.in_file) as fasta_file:
            sequence = ''
            # Find first header.
            line = fasta_file.readline()
            while not line.startswith('>'):
                line = fasta_file.readline()
                if not line:
                    error = """ This file provided is not in proper fasta format.
                    In addition to the usual fasta conventions, be sure that there are
                    no blank lines in the file.
                    """
                    raise RuntimeError(error)
            header = line.rstrip()

            # Get sequence associated with that header.
            for line in fasta_file:
                if line.startswith('>'):
                    # Once the sequence is over, (next header begins),
                    # yield initial header and sequence.
                    yield header, sequence
                    header = line.rstrip()
                    sequence = ''
                else:
                    sequence += ''.join(line.rstrip().split())
        yield header, sequence