from __future__ import division
import time

import numpy as np

from InterscaffoldAlignment import InterscaffoldAlignment


def parse_sam(in_sams, headers):
    """
    I need to speed this up a lot!
    :param in_sam:
    :param headers:
    :return:
    """
    index = 0

    alignments = {}
    for sam in in_sams:
        with open(sam, 'r') as f:
            for line in f:
                index += 1

                if index % 2 != 0:
                    continue

                if index % 1000000 == 0:
                    log('Processed %r alignments' % index)
                if line.startswith('@'):
                    continue
                L1 = line.split('\t')

                # Filter alignments. First see if there was actually an alignment
                if L1[2] == '*':
                    continue

                # Next, filter alignments that aligned within a single scaffold
                if L1[6] == '=':
                    continue

                # Finally, make sure that the reference headers for both mates are in the specified list
                if L1[2] in headers and L1[6] in headers:
                    scaffold_1 = headers.index(L1[2])
                    scaffold_2 = headers.index(L1[6])
                    if scaffold_1 < scaffold_2:
                        scaffold_pair = (scaffold_1, scaffold_2)
                    else:
                        scaffold_pair = (scaffold_2, scaffold_1)
                    # Bind the coordinate to the scaffold header
                    coord_1 = (scaffold_1, int(L1[3]))
                    coord_2 = (scaffold_2, int(L1[7]))
                    if scaffold_pair in alignments.keys():
                        alignments[scaffold_pair].add_alignment(coord_1, coord_2)
                    else:
                        alignments[scaffold_pair] = InterscaffoldAlignment(coord_1, coord_2)

    return alignments


def log(message):
    """ Log messages to standard output. """
    print time.ctime() + '  --  ' + message


# Redo this so it takes in a pandas dataframe
def _get_explained_variance(samples, total_mean, num_groups):
    """

    :param samples:
    :param total_mean:
    :param num_groups:
    :return:
    """
    this_sample_mean = np.mean(samples)
    num_obs = len(samples)
    numerator = num_obs * (this_sample_mean - total_mean) ** 2
    return numerator/(num_groups-1)


def _get_unexplained_variance():
    pass