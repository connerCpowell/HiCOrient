__author__ = 'malonge'

from ScaffoldBlock import ScaffoldBlock


class ScaffoldBlockPair(object):
    """
    This object represents a pair of scaffolds and the alignments between them.
    The main utility of this class is the ability to get the collection of alignments
    between two scaffolds. Also, this class defines utilities to get the theoretical alignments
    associated with the reverse complementation of either or both of the scaffolds of a given pair.
    """

    def __init__(self, block_a, block_b):
        # Initialize the two blocks of the pair.
        if isinstance(block_a, ScaffoldBlock):
            self.block_a = block_a
        else:
            raise ValueError('Must instantiate a ScaffoldBlockPair with two ScaffoldBlock objects, not %s' % str(type(block_a)))

        if isinstance(block_b, ScaffoldBlock):
            self.block_b = block_b
        else:
            raise ValueError('Must instantiate a ScaffoldBlockPair with two ScaffoldBlock objects, not %s' % str(type(block_b)))

        # Make a data structure to hold alignments between these two blocks
        inter_block_alignments = {}

    def __repr__(self):
        return '<ScaffoldBlockPair: ' + str(self.block_a) + ' - ' + str(self.block_b) + '>'

    def _get_block_a_coord(self, scaffold, coord):
        """
        Given a coordinate relative to a scaffold_a, return a coordinate that
        is relative to the scaffolds position within the whole block.
        :param scaffold:
        :param coord:
        :return:
        """
        try:
            block_position = self.block_a.scaffolds.index(scaffold)
        except IndexError:
            raise ValueError('Scaffold %r is not in %s.' %(scaffold, str(self.block_a)))
        pre_block_length = 0
        for i in range(block_position):
            pre_block_length += self.block_a.lengths[i]

        # Check if this scaffold has been flipped. Handle coordinate accordingly.
        if self.block_a.orientations[block_position] == '+':
            return pre_block_length + coord
        else:
            return pre_block_length + self.block_a.lengths[block_position] - coord

    def _get_block_a_reverse_coord(self, scaffold, coord):
        """
        Given a coordinate relative to a scaffold_a, return a coordinate that
        is relative to the scaffolds position within the whole block.
        In this case, the value returned is the coordinate of a theoretically reverse
        complemented block.
        :param scaffold:
        :param coord:
        :return:
        """
        try:
            block_position = self.block_a.scaffolds.index(scaffold)
        except IndexError:
            raise ValueError('Scaffold %r is not in %s.' % (scaffold, str(self.block_a)))
        pre_block_length = 0
        for i in range(block_position):
            pre_block_length += self.block_a.lengths[i]

        # Check if this scaffold has been flipped. Handle coordinate accordingly.
        if self.block_a.orientations[block_position] == '-':
            return pre_block_length + coord
        else:
            return pre_block_length + self.block_a.lengths[block_position] - coord

    def _get_block_b_coord(self, scaffold, coord):
        """
        Given a coordinate relative to a scaffold_a, return a coordinate that
        is relative to the scaffolds position within the whole block.
        :param scaffold:
        :param coord:
        :return:
        """
        try:
            block_position = self.block_b.scaffolds.index(scaffold)
        except IndexError:
            raise ValueError('Scaffold %r is not in %s.' %(scaffold, str(self.block_b)))
        pre_block_length = 0
        for i in range(block_position):
            pre_block_length += self.block_b.lengths[i]

        # Check if this scaffold has been flipped. Handle coordinate accordingly.
        if self.block_b.orientations[block_position] == '+':
            return pre_block_length + coord
        else:
            return pre_block_length + self.block_b.lengths[block_position] - coord

    def _get_block_b_reverse_coord(self, scaffold, coord):
        """
        Given a coordinate relative to a scaffold_a, return a coordinate that
        is relative to the scaffolds position within the whole block.
        In this case, the value returned is the coordinate of a theoretically reverse
        complemented block.
        :param scaffold:
        :param coord:
        :return:
        """
        try:
            block_position = self.block_b.scaffolds.index(scaffold)
        except IndexError:
            raise ValueError('Scaffold %r is not in %s.' %(scaffold, str(self.block_b)))
        pre_block_length = 0
        for i in range(block_position):
            pre_block_length += self.block_b.lengths[i]

        # Check if this scaffold has been flipped. Handle coordinate accordingly.
        if self.block_b.orientations[block_position] == '-':
            return pre_block_length + coord
        else:
            return pre_block_length + self.block_b.lengths[block_position] - coord

    def get_interscaffold_distances(self, alignments, reverse_a=False, reverse_b=False):
        """

        :return:
        """
        all_distances = []
        # Get every possible pairing of scaffolds from block_a and block_b
        all_pairs = []
        for i in self.block_a.scaffolds:
            for j in self.block_b.scaffolds:
                all_pairs.append((i, j))

        # Get all of the alignments between these two scaffolds.
        for pair in all_pairs:
            if pair in alignments.keys():
                for i, j in zip(alignments[pair].pos_a, alignments[pair].pos_b):
                    if not reverse_a:
                        block_a_coord = self._get_block_a_coord(pair[0], i)
                    else:
                        block_a_coord = self._get_block_a_reverse_coord(pair[0], i)
                    if not reverse_b:
                        block_b_coord = self._get_block_b_coord(pair[1], j)
                    else:
                        block_b_coord = self._get_block_b_reverse_coord(pair[1], j)
                    distance = sum(self.block_a.lengths) - block_a_coord + block_b_coord
                    all_distances.append(distance)

        return all_distances