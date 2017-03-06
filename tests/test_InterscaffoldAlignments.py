__author__ = 'malonge'
import unittest

from hic_orientation.InterscaffoldAlignment import InterscaffoldAlignment


class InterscaffoldAlignmentTest(unittest.TestCase):

    def setUp(self):
        self.first_ISA = InterscaffoldAlignment(0, 2, 1, 4)
        self.second_ISA = InterscaffoldAlignment(1, 9, 0, 5)

    def test_init_empty(self):
        with self.assertRaises(TypeError):
            x = InterscaffoldAlignment()

    def test_init_wrong_value(self):
        with self.assertRaises(TypeError):
            x = InterscaffoldAlignment('foo', 'bar', 'foo', 'bar')

    def test_init_same_scaffold(self):
        with self.assertRaises(ValueError):
            x = InterscaffoldAlignment(0, 2, 0, 4)

    def test_first_scaffold_is_smaller(self):
        self.assertEqual(self.first_ISA._scaffold_a, 0)
        self.assertEqual(self.first_ISA._scaffold_b, 1)
        self.assertEqual(self.second_ISA._scaffold_a, 0)
        self.assertEqual(self.second_ISA._scaffold_b, 1)

    def test_add_alignment_normal(self):
        self.second_ISA.add_alignment(1, 3, 0, 1)
        self.assertEqual(self.second_ISA.pos_a, [5, 1])
        self.assertEqual(self.second_ISA.pos_b, [9, 3])