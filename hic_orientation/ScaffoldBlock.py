__author__ = 'malonge'


class ScaffoldBlock(object):
    """
    """

    def __init__(self, scaffold, length):
        self.scaffolds = [scaffold]
        self.orientations = ['+']
        self.lengths = [int(length)]
        self.oriented = False
        self.is_fixed = False

        # Add orientations

    def __repr__(self):
        str_list = [str(i) for i in self.scaffolds]
        return "<ScaffoldBlock: " +",".join(str_list) + ">"

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
        :return:
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
        if self.is_fixed:
            raise ValueError('Cannot reverse complement a fixed block. %s' % (str(self)))
        reverse_orientations = []
        for i in self.orientations:
            if i == '+':
                reverse_orientations.append('-')
            else:
                reverse_orientations.append('+')
        self.orientations = reverse_orientations
        self.oriented = True