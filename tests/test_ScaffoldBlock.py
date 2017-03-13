__author__ = 'malonge'
import unittest

from hic_orientation.ScaffoldBlock import ScaffoldBlock


class ScaffoldBlockTest(unittest.TestCase):

    def setUp(self):
        self.first_scaffold = ScaffoldBlock(0, 10)
        self.second_scaffold = ScaffoldBlock(1, 11)
        self.third_scaffold = ScaffoldBlock(2, 12)

    def test_init_empty_header(self):
        with self.assertRaises(TypeError):
            x = ScaffoldBlock()

    def test_init_string_header(self):
        with self.assertRaises(TypeError):
            x = ScaffoldBlock('0', 10)

    def test_init_string_length(self):
        with self.assertRaises(TypeError):
            x = ScaffoldBlock(0, '10')

    def test_init_proper(self):
        self.assertEqual(self.first_scaffold.scaffolds, [0])
        self.assertEqual(self.first_scaffold.scaffolds, [0])
        self.assertEqual(self.first_scaffold.lengths, [10])
        self.assertEqual(self.first_scaffold.orientations, ['+'])

    def test_join_non_consecutive(self):
        with self.assertRaises(ValueError):
            self.first_scaffold.join(self.third_scaffold)

    def test_join_consecutive(self):
        self.first_scaffold.join(self.second_scaffold)
        self.assertEqual(self.first_scaffold.scaffolds, [0, 1])
        self.first_scaffold.join(self.third_scaffold)
        self.assertEqual(self.first_scaffold.scaffolds, [0, 1, 2])

    def test_one_reverse_complement(self):
        self.assertEqual(self.first_scaffold.orientations, ['+'])
        self.first_scaffold.reverse_complement()
        self.assertEqual(self.first_scaffold.orientations, ['-'])

    def test_two_same_reverse_complement(self):
        self.assertEqual(self.first_scaffold.orientations, ['+'])
        self.first_scaffold.join(self.second_scaffold)
        self.first_scaffold.reverse_complement()
        self.assertEqual(self.first_scaffold.orientations, ['-', '-'])

    def test_two_diff_reverse_complement(self):
        self.assertEqual(self.first_scaffold.orientations, ['+'])
        self.assertEqual(self.second_scaffold.orientations, ['+'])
        self.second_scaffold.reverse_complement()
        self.assertEqual(self.second_scaffold.orientations, ['-'])
        self.first_scaffold.join(self.second_scaffold)
        self.assertEqual(self.first_scaffold.orientations, ['+', '-'])
        self.first_scaffold.reverse_complement()
        self.assertEqual(self.first_scaffold.orientations, ['-', '+'])

    def test_two_diff_reverse_complement_twice(self):
        self.assertEqual(self.first_scaffold.orientations, ['+'])
        self.assertEqual(self.second_scaffold.orientations, ['+'])
        self.second_scaffold.reverse_complement()
        self.assertEqual(self.second_scaffold.orientations, ['-'])
        self.first_scaffold.join(self.second_scaffold)
        self.assertEqual(self.first_scaffold.orientations, ['+', '-'])
        self.first_scaffold.reverse_complement()
        self.assertEqual(self.first_scaffold.orientations, ['-', '+'])
        self.first_scaffold.reverse_complement()
        self.assertEqual(self.first_scaffold.orientations, ['+', '-'])

if __name__ == '__main__':
    unittest.main()