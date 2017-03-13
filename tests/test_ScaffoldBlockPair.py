__author__ = 'malonge'
import unittest

from hic_orientation.ScaffoldBlock import ScaffoldBlock
from hic_orientation.ScaffoldBlockPair import ScaffoldBlockPair
from hic_orientation.InterscaffoldAlignment import InterscaffoldAlignment


class ScaffoldBlockPairTest(unittest.TestCase):

    def setUp(self):
        # Make fake alignments
        self.alignments = dict()
        self.alignments[(0, 1)] = InterscaffoldAlignment(0, 3, 1, 7)
        self.alignments[(1, 2)] = InterscaffoldAlignment(1, 2, 2, 8)
        self.alignments[(0, 2)] = InterscaffoldAlignment(0, 1, 2, 6)
        self.alignments[(1, 3)] = InterscaffoldAlignment(1, 2, 3, 5)


        self.first_scaffold = ScaffoldBlock(0, 10)
        self.second_scaffold = ScaffoldBlock(1, 11)
        self.third_scaffold = ScaffoldBlock(2, 12)
        self.fourth_scaffold = ScaffoldBlock(3, 15)
        self.third_scaffold.join(self.fourth_scaffold)

        self.first_scaffold_pair = ScaffoldBlockPair(self.first_scaffold, self.second_scaffold)
        self.second_scaffold_pair = ScaffoldBlockPair(self.second_scaffold, self.third_scaffold)

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
    def test_get_ISD_2_scaf_ff(self):
        alns = self.first_scaffold_pair.get_interscaffold_distances(self.alignments, reverse_a=False, reverse_b=False)
        self.assertEqual(alns, [14])

    def test_get_ISD_3_scaf_ff(self):
        alns = self.second_scaffold_pair.get_interscaffold_distances(self.alignments, reverse_a=False, reverse_b=False)
        self.assertEqual(alns, [17, 26])

    def test_get_ISD_3_scaf_fr(self):
        alns = self.second_scaffold_pair.get_interscaffold_distances(self.alignments, reverse_a=False, reverse_b=True)
        self.assertEqual(alns, [13, 31])

    def test_get_ISD_3_scaf_rf(self):
        alns = self.second_scaffold_pair.get_interscaffold_distances(self.alignments, reverse_a=True, reverse_b=False)
        self.assertEqual(alns, [10, 19])

    def test_get_ISD_3_scaf_rr(self):
        alns = self.second_scaffold_pair.get_interscaffold_distances(self.alignments, reverse_a=True, reverse_b=True)
        self.assertEqual(alns, [10, 19])