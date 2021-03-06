#!/usr/bin/env python
__author__ = 'malonge'

import numpy as np

from hic_orientation.ScaffoldBlock import ScaffoldBlock
from hic_orientation.ScaffoldBlockPair import ScaffoldBlockPair
from hic_orientation.utilities import log


def _is_outlier(n, p_25, p_75):
    iqr = p_75 - p_25
    lower_bound = p_25 - 1.5 * iqr
    upper_bound = p_75 + 1.5 * iqr
    return n <= lower_bound or n >= upper_bound


def _get_Q1(dist):
    return np.percentile(dist, 25)


def _get_Q3(dist):
    return np.percentile(dist, 75)


def iterate_pairs(iterable, off_set=False):
    """

    :param iterable:
    :return:
    """
    if off_set:
        start = 1
    else:
        start = 0
    for i in range(start, len(iterable), 2):
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


def set_cheats(in_cheat_file, scaffold_blocks, scaffold_list):
    """
    This needs to be done when there is one scaffold block for each scaffold.
    :param in_cheat_file:
    :param scaffold_blocks:
    :return:
    """
    with open(in_cheat_file, 'r') as f:
        for line, block in zip(f, scaffold_blocks):
            cheat_scaffold, cheat_orientation = line.rstrip().split('\t')
            cheat_scaffold_index = scaffold_list.index(cheat_scaffold)
            if cheat_scaffold_index != block.scaffolds[0]:
                raise ValueError('Cheat file and scaffolds are out of order %s and %s.' % (cheat_scaffold, scaffold_list[block.scaffolds[0]]))
            if cheat_orientation == '?':
                continue
            elif cheat_orientation == '-':
                block.reverse_complement()
                block.oriented = True
                block.is_fixed = True
            elif cheat_orientation == '+':
                block.oriented = True
                block.is_fixed = True
            else:
                raise ValueError('Orientation may only be ?, -, or +')
    return scaffold_blocks


def remove_outliers(dist):
    if not isinstance(dist, list):
        raise TypeError('Can only remove outliers from a list.')
    if not dist:
        return dist

    p_25 = _get_Q1(dist)
    p_75 = _get_Q3(dist)
    return [i for i in dist if not _is_outlier(i, p_25, p_75)]


def orient_adjacent_pairs(in_scaffold_blocks, in_scaffolds, alignments, n=100):
    """

    :param in_scaffold_blocks:
    :param in_scaffolds:
    :param alignments:
    :param n: Minimum sample size needed to orient a ScaffoldBlockPair
    :return:
    """
    iteration = 0
    off_set = False
    tried_off_set = False
    while True:
        log('Beginning iteration %r of phase 1.' % iteration)
        write_summary(in_scaffold_blocks, in_scaffolds, 'iteration_' + str(iteration) + '_results.txt')
        iteration += 1

        # Take pairs, in order, from the scaffold block list and start comparing them.
        new_scaffold_block_list = []
        if off_set:
            new_scaffold_block_list.append(in_scaffold_blocks[0])
        changes = False
        for block_a, block_b in iterate_pairs(in_scaffold_blocks, off_set=off_set):
            # Instantiate a ScaffoldBlockPair object with these two blocks.
            this_block_pair = ScaffoldBlockPair(block_a, block_b)

            # Get the interscaffold alignment distances for both cases.
            f_f_alignments = this_block_pair.get_interscaffold_distances(alignments)
            f_f_alignments = remove_outliers(f_f_alignments)

            f_r_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_b=True)
            f_r_alignments = remove_outliers(f_r_alignments)

            r_f_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_a=True)
            r_f_alignments = remove_outliers(r_f_alignments)

            r_r_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_a=True, reverse_b=True)
            r_r_alignments = remove_outliers(r_r_alignments)

            # Compare the mean alignment distance for all 4 possible orientations.
            if all([len(f_f_alignments) >= n, len(f_r_alignments) >= n, len(r_f_alignments) >= n, len(r_r_alignments) >= n]):

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
                    log('With %r alignments between them, Scaffold(s) %s were oriented relative to scaffold(s) %s.' % (len(f_f_alignments), str(block_a), str(block_b)))
                    block_a.join(block_b)
                    block_a.is_fixed = True
                    new_scaffold_block_list.append(block_a)
                    changes = True
                elif smallest_distance == np.mean(f_r_alignments):
                    # Make sure not to reverse complement blocks that are fixed.
                    if not block_b.is_fixed:
                        log('With %r alignments between them, Scaffold(s) %s were oriented relative to scaffold(s) %s.' % (len(f_r_alignments), str(block_a), str(block_b)))
                        block_b.reverse_complement()
                        block_a.join(block_b)
                        block_a.is_fixed = True
                        new_scaffold_block_list.append(block_a)
                        changes = True
                    else:
                        new_scaffold_block_list.append(block_a)
                        new_scaffold_block_list.append(block_b)
                elif smallest_distance == np.mean(r_f_alignments):
                    # Make sure not to reverse complement blocks that are fixed.
                    if not block_a.is_fixed:
                        log('With %r alignments between them, Scaffold(s) %s were oriented relative to scaffold(s) %s.' % (len(r_f_alignments), str(block_a), str(block_b)))
                        block_a.reverse_complement()
                        block_a.join(block_b)
                        block_a.is_fixed = True
                        new_scaffold_block_list.append(block_a)
                        changes = True
                    else:
                        new_scaffold_block_list.append(block_a)
                        new_scaffold_block_list.append(block_b)
                else:
                    # Make sure not to reverse complement blocks that are fixed.
                    if not any([block_a.is_fixed, block_b.is_fixed]):
                        log('With %r alignments between them, Scaffold(s) %s were oriented relative to scaffold(s) %s.' % (len(r_r_alignments), str(block_a), str(block_b)))
                        block_a.reverse_complement()
                        block_b.reverse_complement()
                        block_a.join(block_b)
                        block_a.is_fixed = True
                        new_scaffold_block_list.append(block_a)
                        changes = True
                    else:
                        new_scaffold_block_list.append(block_a)
                        new_scaffold_block_list.append(block_b)

            else:
                new_scaffold_block_list.append(block_a)
                new_scaffold_block_list.append(block_b)

        # If the scaffold block list is odd, include the odd block out for the next iteration.
        if len(in_scaffold_blocks) % 2 != 0 and not off_set:
            new_scaffold_block_list.append(in_scaffold_blocks[-1])

        if len(in_scaffold_blocks) % 2 == 0 and off_set:
            new_scaffold_block_list.append(in_scaffold_blocks[-1])

        in_scaffold_blocks = new_scaffold_block_list

        # If no changes, try offsetting the scaffold block list so that scaffold blocks can be compared to the
        # other adjacent scaffold block. No improvements are made after comparing each block to both adjacent blocks,
        # move on.
        if not changes:
            if tried_off_set:
                log('No more changes to be made in phase 1.')
                break
            if off_set:
                off_set = False
                tried_off_set = True
            else:
                off_set = True
                tried_off_set = True
        else:
            tried_off_set = False
            off_set = False

    return in_scaffold_blocks


def orient_large_blocks(in_scaffold_blocks, alignments, n=100, m=100000):
    """
    The second phase of HiC based orientation. Here, no attempt will be made to extend blocks.
    Rather, large blocks will be compared to each other and will be oriented in place. This means that
    blocks that are not adjacent can be compared. The difference is that if there is a statistically
    significant orientation found, these orientations will be executed, but blocks will not be extended.
    :param in_scaffold_blocks:
    :param alignments:
    :param n: Minimum sample size needed to orient a ScaffoldBlockPair
    :param m: minimum block size to be considered for this utility
    :return:
    """
    # Get a list of all blocks that either have more than one scaffold, or have a scaffold length >= m
    large_blocks = [this_block for this_block in in_scaffold_blocks if sum(this_block.lengths) >= m or len(this_block.scaffolds) > 1]
    for block_a, block_b in slide_pairs(large_blocks):
        # Instantiate a ScaffoldBlockPair object with these two blocks.
        this_block_pair = ScaffoldBlockPair(block_a, block_b)

        # Get the interscaffold alignment distances for both cases.
        f_f_alignments = this_block_pair.get_interscaffold_distances(alignments)
        f_f_alignments = remove_outliers(f_f_alignments)

        f_r_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_b=True)
        f_r_alignments = remove_outliers(f_r_alignments)

        r_f_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_a=True)
        r_f_alignments = remove_outliers(r_f_alignments)

        r_r_alignments = this_block_pair.get_interscaffold_distances(alignments, reverse_a=True, reverse_b=True)
        r_r_alignments = remove_outliers(r_r_alignments)

        # Compare the mean alignment distance for all 4 possible orientations.
        if all([len(f_f_alignments) >= n, len(f_r_alignments) >= n, len(r_f_alignments) >= n, len(r_r_alignments) >= n]):
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
                # Orientations are already accurate
                block_a.oriented = True
                block_b.oriented = True
                block_a.is_fixed = True
                block_b.is_fixed = True
                log('With %r alignments between them, Scaffold(s) %s were oriented relative to scaffold(s) %s.' % (len(f_f_alignments), str(block_a), str(block_b)))
            elif smallest_distance == np.mean(f_r_alignments):
                if not in_scaffold_blocks[in_scaffold_blocks.index(block_b)].is_fixed:
                    in_scaffold_blocks[in_scaffold_blocks.index(block_b)].reverse_complement()
                    block_a.oriented = True
                    block_b.oriented = True
                    block_a.is_fixed = True
                    block_b.is_fixed = True
                    log('With %r alignments between them, Scaffold(s) %s were oriented relative to scaffold(s) %s.' % (len(f_r_alignments), str(block_a), str(block_b)))
            elif smallest_distance == np.mean(r_f_alignments):
                if not in_scaffold_blocks[in_scaffold_blocks.index(block_a)].is_fixed:
                    in_scaffold_blocks[in_scaffold_blocks.index(block_a)].reverse_complement()
                    block_a.oriented = True
                    block_b.oriented = True
                    block_a.is_fixed = True
                    block_b.is_fixed = True
                    log('With %r alignments between them, Scaffold(s) %s were oriented relative to scaffold(s) %s.' % (len(r_f_alignments), str(block_a), str(block_b)))
            else:
                if not any([in_scaffold_blocks[in_scaffold_blocks.index(block_a)].is_fixed, in_scaffold_blocks[in_scaffold_blocks.index(block_b)].is_fixed]):
                    in_scaffold_blocks[in_scaffold_blocks.index(block_a)].reverse_complement()
                    in_scaffold_blocks[in_scaffold_blocks.index(block_b)].reverse_complement()
                    block_a.oriented = True
                    block_b.oriented = True
                    block_a.is_fixed = True
                    block_b.is_fixed = True
                    log('With %r alignments between them, Scaffold(s) %s were oriented relative to scaffold(s) %s.' % (len(r_r_alignments), str(block_a), str(block_b)))

    return in_scaffold_blocks


def main():

    import argparse

    from hic_orientation.utilities import parse_sam

    parser = argparse.ArgumentParser(description='Orient anchored/ordered scaffolds with chromatin interaction data.')

    parser.add_argument('scaffolds', metavar='<scaffolds.txt>', type=str,
                        help='An ordered list of scaffold headers. First column is scaffold header, second is scaffold length.')
    parser.add_argument('alignments', metavar='<alignments.sam>', nargs='+',
                        type=str, help='SAM file(s) containing HiC alignments to the specified scaffolds.')
    parser.add_argument('-n', type=int, default=100, metavar='100',
                        help='The minimum Hi-C event sample size needed to orient a scaffold block pair. Default = 100')
    parser.add_argument('-m', type=int, default=100000, metavar='100000',
                        help='The minimum non-adjacent scaffold size for consideration. Default = 100000')

    parser.add_argument('--cheatWith', type=str, default='', metavar='orientations.txt',
                        help='A tab delimited file with known orientations. 1st column is scaffold name, 2nd column is +,-,?')

    args = parser.parse_args()
    scaffolds_file = args.scaffolds
    alignment_files = args.alignments

    # Get the optional flags
    sample_min = args.n
    min_scaffold_size = args.m
    cheat_file = args.cheatWith

    # Get the ordered list of scaffold headers and associated lengths.
    scaffolds, scaffold_lengths = get_scaffolds_and_lengths(scaffolds_file)

    # Log the unique IDs given to each scaffold.
    for i in scaffolds:
        log('scaffold %s given unique ID %r.' % (i, scaffolds.index(i)))

    # Make a list of scaffold block objects.
    scaffold_block_list = [ScaffoldBlock(scaffolds.index(i), j) for i, j in zip(scaffolds, scaffold_lengths)]

    # Add cheat info if it is available
    if cheat_file:
        log('Cheating with %s' % cheat_file)
        scaffold_block_list = set_cheats(cheat_file, scaffold_block_list, scaffolds)

    # Parse the alignment data
    # Send each sam/bam file to a method that will return the parsed info as a dictionary.
    # The key will be the set of 2 scaffolds with alignments, and the value will be a corresponding
    # InterscaffoldAlignment object.
    these_alignments = parse_sam(alignment_files, scaffolds)

    # Run the first phase of orientation - the orientation of adjacent pairs.
    scaffold_block_list = orient_adjacent_pairs(scaffold_block_list, scaffolds, these_alignments, n=sample_min)

    # Phase 2
    log('Beginning phase 2.')
    scaffold_block_list = orient_large_blocks(scaffold_block_list, these_alignments, n=sample_min, m=min_scaffold_size)
    write_summary(scaffold_block_list, scaffolds, 'final_iteration_results.txt')

    # Log the total number of nucleotides that have been oriented.
    total_o = 0
    for block in scaffold_block_list:
        if block.oriented:
            total_o += sum(block.lengths)

    log('The total number of nucleotides oriented is %r' % total_o)

    total = 0
    for block in scaffold_block_list:
        total += sum(block.lengths)

    log('The total number of nucleotides is %r' % total)

if __name__ == "__main__":
    main()