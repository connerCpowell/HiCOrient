__author__ = 'malonge'


class InterscaffoldAlignment(object):
    """

    """
    def __init__(self, coord_a, coord_b):
        """

        :param coord_a: (scaffold_a, pos_a)
        :param coord_b: (scaffold_b, pos_b)
        """
        # Scaffold a always lesser of the two. Ordering will make the query easier.
        self._scaffold_a = None
        self._scaffold_b = None
        self._pos_a = []
        self._pos_b = []

        # Set the values here. A is always smaller
        if coord_a[0] < coord_b[0]:
            self._scaffold_a = coord_a[0]
            self._pos_a.append(coord_a[1])
            self._scaffold_b = coord_b[0]
            self._pos_b.append(coord_b[1])

        elif coord_a[0] > coord_b[0]:
            self._scaffold_a = coord_b[0]
            self._pos_a.append(coord_b[1])
            self._scaffold_b = coord_a[0]
            self._pos_b.append(coord_a[1])
        else:
            raise ValueError('Cannot instantiate this class with a pair of identical scaffolds.')

    def __eq__(self, other):
        if not isinstance(other, InterscaffoldAlignment):
            return False
        return other._scaffold_a == self._scaffold_a and other._scaffold_b == self._scaffold_b

    def __ne__(self, other):
        if not isinstance(other, InterscaffoldAlignment):
            return True
        return other._scaffold_a != self._scaffold_a or other._scaffold_b != self._scaffold_b

    def __repr__(self):
        return "<InterscaffoldAlignment: " + str(self._scaffold_a) + " - " + str(self._scaffold_b) + ">"

    @property
    def pos_a(self):
        return self._pos_a

    @property
    def pos_b(self):
        return self._pos_b

    @property
    def _scaffold_set(self):
        return {self._scaffold_a, self._scaffold_b}

    def add_alignment(self, coord_a, coord_b):
        """

        :param coord_a:
        :param coord_b:
        :return:
        """
        if {coord_a[0], coord_b[0]} != self._scaffold_set:
            raise ValueError()

        if coord_a[0] < coord_b[0]:
            self._pos_a.append(coord_a[1])
            self._pos_b.append(coord_b[1])

        else:
            self._pos_a.append(coord_b[1])
            self._pos_b.append(coord_a[1])

        assert(len(self._pos_a) == len(self._pos_b))