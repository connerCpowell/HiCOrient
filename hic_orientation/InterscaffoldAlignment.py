__author__ = 'malonge'


class InterscaffoldAlignment(object):
    """

    """
    def __init__(self, scaffold_a, coord_a, scaffold_b, coord_b):
        """

        :param scaffold_a:
        :param coord_a:
        :param scaffold_b:
        :param coord_b:
        """

        if not isinstance(scaffold_a, int):
            raise TypeError('scaffold_a must be an integer')

        if not isinstance(scaffold_b, int):
            raise TypeError('scaffold_b must be an integer')

        if not isinstance(coord_a, int):
            raise TypeError('coord_a must be an integer')

        if not isinstance(coord_b, int):
            raise TypeError('coord_b must be an integer')
        # Scaffold a always lesser of the two. Ordering will make the query easier.
        self._scaffold_a = None
        self._scaffold_b = None
        self._pos_a = []
        self._pos_b = []

        # Set the values here. A is always smaller
        if scaffold_a < scaffold_b:
            self._scaffold_a = scaffold_a
            self._pos_a.append(coord_a)
            self._scaffold_b = scaffold_b
            self._pos_b.append(coord_b)

        elif scaffold_a > scaffold_b:
            self._scaffold_a = scaffold_b
            self._pos_a.append(coord_b)
            self._scaffold_b = scaffold_a
            self._pos_b.append(coord_a)
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

    def add_alignment(self, scaffold_a, coord_a, scaffold_b, coord_b):
        """

        :param scaffold_a:
        :param coord_a:
        :param scaffold_b:
        :param coord_b:
        """
        if {scaffold_a, scaffold_b} != self._scaffold_set:
            raise ValueError()

        if scaffold_a < scaffold_b:
            self._pos_a.append(coord_a)
            self._pos_b.append(coord_b)

        else:
            self._pos_a.append(coord_b)
            self._pos_b.append(coord_a)

        assert(len(self._pos_a) == len(self._pos_b))