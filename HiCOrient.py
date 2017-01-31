#!/usr/bin/env python
__author__ = 'malonge'

import itertools

from scipy import stats
import numpy as np

from hic_orientation.ScaffoldBlock import ScaffoldBlock
from hic_orientation.ScaffoldBlockPair import ScaffoldBlockPair


def iterate_pairs(iterable):
    """

    :param iterable:
    :return:
    """
    for i in range(0, len(iterable), 2):
        try:
            a = iterable[i]
            b = iterable[i+1]
            yield a, b

        # If the list is currently an odd length, the last element will be skipped.
        except IndexError:
            pass


def slide_pairs(iterable):
    for i in range(len(iterable) - 1):
        yield iterable[i], iterable[i+1]


def write_summary(scaffold_blocks, scaffold_list, file_name):
    """

    :param scaffold_blocks:
    :param scaffold_list:
    :param file_name:
    :return:
    """
    with open(file_name, 'w') as out_file:
        out_file.write('header\torientation\thic_oriented\n')
        for this_block in scaffold_blocks:
            for scaffold, orientation in zip(this_block.scaffolds, this_block.orientations):
                out_file.write('%s\t%s\t%s\n' %(scaffold_list[scaffold], orientation, str(this_block.oriented)))


def get_scaffolds_and_lengths(in_file):
    scaffolds_list = []
    all_lengths = []
    with open(in_file, 'r') as s_file:
        for line in s_file:
            this_scaffold, length = line.split('\t')
            this_scaffold = this_scaffold.rstrip().replace('>', '')
            length = int(length.rstrip())
            if this_scaffold not in scaffolds_list:
                scaffolds_list.append(this_scaffold)
                all_lengths.append(length)
            else:
                raise ValueError('The scaffold %s appeared twice in the input file.' % this_scaffold)
    return scaffolds_list, all_lengths


def orient_adjacent_pairs(in_scaffold_blocks, in_scaffolds, alignments, n=30):
    """

    :param in_scaffold_blocks:
    :param in_scaffolds:
    :param alignments:
    :param n:
    :return:
    """
    iteration = 0
    while True:
        write_summary(in_scaffold_blocks, in_scaffolds, 'iteration_' + str(iteration) + '_results.txt')
        iteration += 1
        print '**********************\n\n'
        print in_scaffold_blocks
        print(len(in_scaffold_blocks))

        # Take pairs, in order, from the scaffold block list and start comparing them.
        new_scaffold_block_list = []
        changes = False
        for block_a, block_b in iterate_pairs(in_scaffold_blocks):
            # Instantiate a ScaffoldBlockPair object with these two blocks.
            this_block_pair = ScaffoldBlockPair(block_a, block_b)

            # Get the interscaffold alignment distances for both cases. One were the blocks retain their
            # original orientation. One where block_b is reverse complemented.
            f_f_alignments = this_block_pair.get_interscaffold_distances(alignments)
            f_r_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_b=True)
            r_f_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_a=True)
            r_r_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_a=True, reverse_b=True)

            # Perform t-test on these two lists of interscaffold alignment distances.
            if len(f_f_alignments) >= n:
                statistic, p_value = stats.f_oneway(f_f_alignments, f_r_alignments, r_f_alignments, r_r_alignments)

                # If we reject the null hypothesis, reverse complement if necessary and join the two blocks.
                # Otherwise, keep the blocks as is.
                if p_value < 0.05:
                    s1 = ' :: '
                    print block_a, s1, block_b
                    print p_value
                    changes = True

                    # Get the smallest of the means.
                    all_means = sorted(
                        [
                            np.mean(f_f_alignments),
                            np.mean(r_r_alignments),
                            np.mean(f_r_alignments),
                            np.mean(r_f_alignments)
                        ]
                    )
                    smallest_distance = all_means[0]

                    # Make sure that there is one unique smallest mean.
                    if all_means.count(smallest_distance) != 1:
                        continue

                    # Find the orientations which yield the smallest mean and orient accordingly.
                    if smallest_distance == np.mean(f_f_alignments):
                        block_a.join(block_b)
                    elif smallest_distance == np.mean(f_r_alignments):
                        block_b.reverse_complement()
                        block_a.join(block_b)
                    elif smallest_distance == np.mean(r_f_alignments):
                        block_a.reverse_complement()
                        block_a.join(block_b)
                    else:
                        block_a.reverse_complement()
                        block_b.reverse_complement()
                        block_a.join(block_b)
                    new_scaffold_block_list.append(block_a)

                else:
                    new_scaffold_block_list.append(block_a)
                    new_scaffold_block_list.append(block_b)
            else:
                new_scaffold_block_list.append(block_a)
                new_scaffold_block_list.append(block_b)

        # If the scaffold block list is odd, include the odd block out for the next iteration.
        if len(in_scaffold_blocks) % 2 != 0:
            new_scaffold_block_list.append(in_scaffold_blocks[-1])
        in_scaffold_blocks = new_scaffold_block_list

        # If there have been no improvements from the previous iteration, break out of this loop.
        # Move on to next stage: Instead of orienting contiguous scaffolds, orient blocks relative to each other.
        if not changes:
            break

    return in_scaffold_blocks, iteration


def orient_large_blocks(in_scaffold_blocks, in_scaffolds, alignments, iteration, n=30):
    """
    The second phase of HiC based orientation. Here, no attempt will be made to extend blocks.
    Rather, large blocks will be compared to each other and will be oriented in place. This means that
    blocks that are not adjacent can be compared. The difference is that if there is a statistically
    significant orientation found, these orientations will be executed, but blocks will not be extended.
    :param in_scaffold_blocks:
    :param in_scaffolds:
    :param alignments:
    :param n:
    :return:
    """
    # Get a list of all blocks that either have more than one scaffold, or have a scaffold length >= 1 million
    large_blocks = [this_block for this_block in in_scaffold_blocks if sum(this_block.lengths) >= 100000 or len(this_block.scaffolds) > 1]
    for block_a, block_b in slide_pairs(large_blocks):
        # Instantiate a ScaffoldBlockPair object with these two blocks.
        this_block_pair = ScaffoldBlockPair(block_a, block_b)

        # Get the interscaffold alignment distances for all 4 possible alignments.
        f_f_alignments = this_block_pair.get_interscaffold_distances(alignments)
        f_r_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_b=True)
        r_f_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_a=True)
        r_r_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_a=True, reverse_b=True)

        # Perform t-test on these two lists of interscaffold alignment distances.
        if len(f_f_alignments) >= n:
            statistic, p_value = stats.f_oneway(f_f_alignments, f_r_alignments, r_f_alignments, r_r_alignments)
            # If we reject the null hypothesis, reverse complement if necessary, but do not join the two blocks.
            # Otherwise, keep the blocks as is.
            if p_value < 0.05:
                s1 = ' :: '
                print block_a, s1, block_b
                print p_value

                # Get the smallest of the means.
                all_means = sorted(
                    [
                        np.mean(f_f_alignments),
                        np.mean(r_r_alignments),
                        np.mean(f_r_alignments),
                        np.mean(r_f_alignments)
                    ]
                )
                smallest_distance = all_means[0]

                # Make sure that there is one unique smallest mean.
                if all_means.count(smallest_distance) != 1:
                    continue

                block_a.oriented = True
                block_b.oriented = True
                # Find the orientations which yield the smallest mean and orient accordingly.
                if smallest_distance == np.mean(f_f_alignments):
                    print 'ff'
                    pass
                elif smallest_distance == np.mean(f_r_alignments):
                    in_scaffold_blocks[in_scaffold_blocks.index(block_b)].reverse_complement()
                    print 'fr'
                elif smallest_distance == np.mean(r_f_alignments):
                    in_scaffold_blocks[in_scaffold_blocks.index(block_a)].reverse_complement()
                    print 'rf'
                else:
                    in_scaffold_blocks[in_scaffold_blocks.index(block_a)].reverse_complement()
                    in_scaffold_blocks[in_scaffold_blocks.index(block_b)].reverse_complement()
                    print 'rr'

    #iteration += 1
    write_summary(in_scaffold_blocks, in_scaffolds, 'iteration_' + str(iteration) + '_results.txt')
    return in_scaffold_blocks, iteration

if __name__ == "__main__":
    import argparse

    from hic_orientation.utilities import parse_sam
    from hic_orientation.utilities import log

    parser = argparse.ArgumentParser(description='Orient anchored/ordered scaffolds with chromatin interaction data.')

    parser.add_argument('scaffolds', metavar='<scaffolds.txt>', type=str,
                        help='An ordered list of scaffolds. First column is scaffold header, second is scaffold length.')
    parser.add_argument('alignments', metavar='<alignments.sam>', nargs='+',
                        type=str, help='SAM files containing HiC alignments to the specified scaffolds')

    args = parser.parse_args()
    scaffolds_file = args.scaffolds
    # For now, just SAM files.
    alignment_files = args.alignments

    # Get the ordered list of scaffold headers and associated lengths.
    scaffolds, scaffold_lengths = get_scaffolds_and_lengths(args.scaffolds)

    # Make a list of scaffold block objects.
    scaffold_block_list = [ScaffoldBlock(scaffolds.index(i), j) for i, j in zip(scaffolds, scaffold_lengths)]

    # Parse the alignment data
    # Send each sam/bam file to a method that will return the parsed info as a dictionary.
    # The key will be the set of 2 scaffolds with alignments, and the value will be a corresponding
    # InterscaffoldAlignment object.
    these_alignments = parse_sam(alignment_files, scaffolds)

    # Run the first phase of orientation - the orientation of adjacent pairs.
    scaffold_block_list, iter = orient_adjacent_pairs(scaffold_block_list, scaffolds, these_alignments, n=30)

    log('\n\n\n**** Phase 2 **** \n\n\n')
    scaffold_block_list, iter = orient_large_blocks(scaffold_block_list, scaffolds, these_alignments, iter, n=30)


    # Log the total number of nucleotides that have been oriented.
    total_o = 0
    for block in scaffold_block_list:
        if block.oriented:
            total_o += sum(block.lengths)

    log('the total number of nucleotides oriented is %r' % total_o)

    total = 0
    for block in scaffold_block_list:
        total += sum(block.lengths)

    log('the total number of nucleotides is %r' % total)





