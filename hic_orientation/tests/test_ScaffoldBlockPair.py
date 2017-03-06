__author__ = 'malonge'
import unittest

from hic_orientation.ScaffoldBlock import ScaffoldBlock
from hic_orientation.ScaffoldBlockPair import ScaffoldBlockPair


class ScaffoldBlockPairTest(unittest.TestCase):

    def setUp(self):
        self.first_scaffold = ScaffoldBlock(0, 10)
        self.second_scaffold = ScaffoldBlock(1, 11)
        self.third_scaffold = ScaffoldBlock(2, 12)

        self.first_scaffold_pair = ScaffoldBlockPair(self.first_scaffold, self.second_scaffold)

        self.second_scaffold.join(self.third_scaffold)
        self.second_scaffold_pair = ScaffoldBlockPair(self.first_scaffold, self.second_scaffold)

    def test_init_empty(self):
        with self.assertRaises(TypeError):
            x = ScaffoldBlockPair()

    def test_init_one_block(self):
        with self.assertRaises(TypeError):
            x = ScaffoldBlockPair(self.first_scaffold)

    def test_init_three_block(self):
        with self.assertRaises(TypeError):
            x = ScaffoldBlockPair(self.first_scaffold, self.second_scaffold, self.first_scaffold)

    def test_init_wrong_value(self):
        with self.assertRaises(ValueError):
            x = ScaffoldBlockPair('string1', 'string2')


    # get_interscaffold_distances
    #def test_get_ISD_ff(self):
    #    self.first_scaffold_pair.get_interscaffold_distances()