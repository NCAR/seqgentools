
import unittest

import seqgentools as sgt
import itertools as it

MAX = 100

class CompoundSequenceTests(unittest.TestCase):

    def setUp(self):
        # Wrappers of list, set, tuple, dict, ...
        # Slice, Range, Count, Cycle, Repeat
        # Product, Permutations, Combinations, CombinationsR
        # PermutationRange, CombinationRange
            
        # create pairs of (sgt, it)

        # getitem, length, copy, deepcopy, +, index, in, iter, get
        pass

    def tearDown(self):
        pass

    def _iter_equals(self, iterable1, iterable2, N=True):

        while N:
            val = next(iterable1, None) 
            ref = next(iterable2, None) 
            if val is None and ref is None:
                break
            self.assertEqual(val, ref)
            if N is not True:
                N -= 1

test_classes = (CompoundSequenceTests,)

