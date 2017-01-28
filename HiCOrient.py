#!/usr/bin/env python
__author__ = 'malonge'


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


def write_summary(scaffold_blocks, scaffold_list, file_name):
    """

    :param scaffold_blocks:
    :param scaffold_list:
    :param file_name:
    :return:
    """
    with open(file_name, 'w') as out_file:
        out_file.write('header\torientation\thic_oriented\n')
        in_block = False
        for block in scaffold_blocks:
            if len(block.scaffolds) > 1:
                in_block = True
            else:
                in_block = False

            for scaffold, orientation in zip(block.scaffolds, block.orientations):
                out_file.write('%s\t%s\t%s\n' %(scaffold_list[scaffold], orientation, str(in_block)))


def get_scaffolds_and_lengths(in_file):
    scaffolds = []
    scaffold_lengths = []
    with open(in_file, 'r') as scaffolds_file:
        for line in scaffolds_file:
            this_scaffold, length = line.split('\t')
            this_scaffold = this_scaffold.rstrip().replace('\t', '')
            length = int(length.rstrip())
            if this_scaffold not in scaffolds:
                scaffolds.append(this_scaffold)
                scaffold_lengths.append(length)
            else:
                raise ValueError('The scaffold %s appeared twice in the input file.' % this_scaffold)
    return scaffolds, scaffold_lengths


if __name__ == "__main__":
    import argparse

    from scipy import stats
    import numpy as np

    from hic_orientation.utilities import parse_sam
    from hic_orientation.utilities import log
    from hic_orientation.ScaffoldBlock import ScaffoldBlock
    from hic_orientation.ScaffoldBlockPair import ScaffoldBlockPair

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

    iteration = 0
    while True:
        write_summary(scaffold_block_list, scaffolds, 'iteration_' + str(iteration) + '_results.txt')
        iteration += 1
        print '**********************\n\n'
        print scaffold_block_list
        print(len(scaffold_block_list))

        # Take pairs, in order, from the scaffold block list and start comparing them.
        new_scaffold_block_list = []
        # Right now, the last element of an odd list is being left out.
        changes = False
        for block_a, block_b in iterate_pairs(scaffold_block_list):
            # Instantiate a ScaffoldBlockPair object with these two blocks.
            this_block_pair = ScaffoldBlockPair(block_a, block_b)

            # Get the interscaffold alignment distances for both cases. One were the blocks retain their
            # original orientation. One where block_b is reverse complemented.
            forward_alignments = this_block_pair.get_interscaffold_distances(these_alignments)
            reverse_alignments = this_block_pair.get_interscaffold_distances(these_alignments, reverse_b=True)

            # Perform t-test on these two lists of interscaffold alignment distances.
            if len(forward_alignments) > 30 and len(reverse_alignments) > 30:
                statistic, p_value = stats.ttest_ind(forward_alignments, reverse_alignments)

                # If we reject the null hypothesis, reverse complement if necessary and join the two blocks.
                # Otherwise, keep the blocks as is.
                if p_value < 0.05:
                    changes = True
                    if np.mean(forward_alignments) < np.mean(reverse_alignments):
                        block_a.join(block_b)
                    else:
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
        if len(scaffold_block_list) % 2 != 0:
            new_scaffold_block_list.append(scaffold_block_list[-1])
        scaffold_block_list = new_scaffold_block_list

        # If there have been no improvements from the previous iteration, break out of this loop.
        # Move on to next stage: Instead of orienting contiguous scaffolds, orient blocks relative to each other.
        if not changes:
            break

    # Log the total number of nucleotides that have been oriented.
    total_o = 0
    for block in scaffold_block_list:
        if len(block.scaffolds) > 1:
            total_o += sum(block.lengths)

    log('the total number of nucleotides oriented is %r' % total_o)

    total = 0
    for block in scaffold_block_list:
        total += sum(block.lengths)

    log('the total number of nucleotides is %r' % total)





