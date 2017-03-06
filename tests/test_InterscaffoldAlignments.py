__author__ = 'malonge'
import unittest

from hic_orientation.InterscaffoldAlignment import InterscaffoldAlignment


class InterscaffoldAlignmentTest(unittest.TestCase):

    def setUp(self):
        x1 = (0, 2)
        x2 = (1, 4)
        x3 = (0, 5)
        x4 = (1, 9)
        self.first_ISA = InterscaffoldAlignment(x1, x2)
        self.second_ISA = InterscaffoldAlignment(x1, x2)
        self.second_ISA.add_alignment(x3, x4)

    def test_init_empty(self):
        with self.assertRaises(TypeError):
            x = InterscaffoldAlignment()

    # Might want to change the way this class is initialized
    # scaffold_a, coord_a, scaffold_b, coord_b
    #def test_init_wrong_value(self):
    #    with self.assertRaises(ValueError):
    #        x = InterscaffoldAlignment(1, 2)