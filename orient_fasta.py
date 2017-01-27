#!/usr/bin/env python
__author__ = 'malonge'

complements = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C',
    'N': 'N',
    'U': 'A',
    'R': 'Y',
    'Y': 'R',
    'S': 'S',
    'W': 'W',
    'K': 'M',
    'M': 'K',
    'B': 'V',
    'V': 'B',
    'D': 'H',
    'H': 'D'
}


def reverse_complement(seq):
    """
    Reverse complement a nucleotide sequence.
    :param seq: Sequence to be reverse complemented
    :return: A reverse complemented sequence
    """
    rc_seq = ''
    for nuc in seq[::-1]:
        rc_seq += complements[nuc]
    return rc_seq

if __name__ == "__main__":
    import argparse
    from hic_orientation.SeqReader import SeqReader

    parser = argparse.ArgumentParser(description='Orient scaffolds fasta file according to HiCOrient output.')
    parser.add_argument('scaffolds', metavar="<scaffolds.fasta>", type=str, help='fasta file containing oriented sequences')
    parser.add_argument('orientations', metavar="<orientations.txt>", type=str, help='HiCOrient results tsv file')
    parser.add_argument('--prefix', type=str, help='Prefix to use for output files.')

    args = parser.parse_args()
    fasta_file = args.scaffolds
    orientations_file = args.orientations
    prefix = args.prefix

    # Make a dictionary of scaffolds and their orientation
    # Need to go in order and make sure that the order of scaffolds that
    # appear in the fasta are consistent with the order of scaffolds in the
    # results file.
    orientation_dict = {}
    orientations = []
    with open(orientations_file, 'r') as f:
        # Discard header
        f.readline()
        for line in f:
            header, orientation, in_block = line.split('\t')
            orientation_dict[header] = orientation
            orientations.append(header)

    # Open the output fasta file. For each input sequence, reverse complement if needed, then write.
    with open(prefix + '.fasta', 'w') as out_file:
        x = SeqReader(fasta_file)
        for (header, sequence), scaffold in zip(x.parse_fasta(), orientations):
            header = header.replace('>', '')
            # Make sure that the order is consistent across both files.
            if header != scaffold:
                raise ValueError('Fasta and results file are out of order: %s and %s.' % (header, scaffold))
            if header == scaffold:
                if orientation_dict[scaffold] == '+':
                    out_file.write('>' + header + '\n')
                    out_file.write(sequence + '\n')
                else:
                    out_file.write('>' + header + ' - rc\n')
                    out_file.write(reverse_complement(sequence) + '\n')