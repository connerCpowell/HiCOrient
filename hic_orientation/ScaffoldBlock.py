__author__ = 'malonge'


class ScaffoldBlock(object):

    def __init__(self, scaffold, length):
        """
        A ScaffoldBlock is an object designed to bind consecutive scaffolds and their relative orientations
        while still maintaining them as separate entities.

        At minimum, a scaffold block must contain one scaffold.

        :param scaffold: Integer associated with a scaffold header.
        :param length: Length of this scaffold.
        """
        if not isinstance(scaffold, int):
            raise TypeError('Scaffold must be an integer.')

        if not isinstance(length, int):
            raise TypeError('Scaffold must be an integer.')

        if not length:
            raise ValueError('Scaffold length must have length > 0.')

        self.scaffolds = [scaffold]
        self.orientations = ['+']
        self.lengths = [length]
        self.oriented = False
        self.is_fixed = False

    def __repr__(self):
        str_list = [str(i) for i in self.scaffolds]
        return "<ScaffoldBlock: " + ",".join(str_list) + ">"

    def __str__(self):
        str_list = [str(i) for i in self.scaffolds]
        return " ".join(str_list)

    def __eq__(self, block):
        if not isinstance(block, ScaffoldBlock):
            return False

        return all(i == j for i, j in zip(self.scaffolds, block.scaffolds))

    def __ne__(self, block):
        if not isinstance(block, ScaffoldBlock):
            return True

        return any(i != j for i, j in zip(self.scaffolds, block.scaffolds))

    def _is_consecutive(self, in_scaffolds):
        new_scaffolds = self.scaffolds + in_scaffolds
        standard = [i for i in range(new_scaffolds[0], new_scaffolds[-1] + 1)]
        return new_scaffolds == standard

    def join(self, block):
        """
        Join the contents of another block with this one. The join must result in a
        consecutive block of scaffolds. In other words, only adjancent blocks (in terms of order),
        may be joined.
        :param block:
        """
        if not isinstance(block, ScaffoldBlock):
            raise TypeError('Can only join this block to another ScaffoldBlock not to %s.' %(str(type(block))))

        if not self._is_consecutive(block.scaffolds):
            raise ValueError('Can only join consecutive scaffolds. %s and %s are not consecutive.' %(str(self), str(block)))

        for i in block.scaffolds:
            self.scaffolds.append(i)

        for i in block.orientations:
            self.orientations.append(i)

        for i in block.lengths:
            self.lengths.append(i)

        self.oriented = True

        if block.is_fixed:
            self.is_fixed = True

    def reverse_complement(self):
        """ Reverse complement every scaffold in this block. """
        # Make sure that this block has not been fixed.
        if self.is_fixed:
            raise RuntimeError('Cannot reverse complement a fixed block. %s' % (str(self)))

        # Iterate through each orientation and reverse complement.
        reverse_orientations = []
        for i in self.orientations:
            if i == '+':
                reverse_orientations.append('-')
            else:
                reverse_orientations.append('+')
        self.orientations = reverse_orientations
        self.oriented = True