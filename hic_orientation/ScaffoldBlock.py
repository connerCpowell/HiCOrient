__author__ = 'malonge'


class ScaffoldBlock(object):
    """
    This class represents a block of ordered scaffolds. The purpose of this representation is to
    fix orientations into oriented blocks. In other words, if two scaffolds are oriented, they can
    become a block, and the orientation of these two scaffolds relative to each other will always stay fixed.
    All chromosomes start with each scaffold as its own block. Accordingly, at minimum, one scaffold and
    its length is needed to instantiate this object. A chromosome that is 100% oriented will, at the
    end be one large block made up of every scaffold.
    """

    def __init__(self, scaffold, length):
        """

        :param scaffold:
        :param length:
        """
        self.scaffolds = [scaffold]
        self.orientations = ['+']
        self.lengths = [int(length)]
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

    def join(self, block):
        """
        Join the contents of another block with this one.
        :param block:
        """
        if not isinstance(block, ScaffoldBlock):
            raise ValueError('Can only join this block to another ScaffoldBlock not to %s.' %(str(type(block))))

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
            raise ValueError('Cannot reverse complement a fixed block. %s' % (str(self)))

        # Iterate through each orientation and reverse complement.
        reverse_orientations = []
        for i in self.orientations:
            if i == '+':
                reverse_orientations.append('-')
            else:
                reverse_orientations.append('+')
        self.orientations = reverse_orientations
        self.oriented = True