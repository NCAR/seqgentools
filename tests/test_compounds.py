# coding: utf-8

from __future__ import (unicode_literals, print_function,
        division)

import sys
import unittest

import seqgentools as sgt
import itertools as it

MAX = 100

l = [["foo", "a", "a",], ["bar", "a", "b"], ["lee", "b", "b"]]

class TestGenerator(type):

    def __new__(mcs, name, bases, namespace):

        # create test function
        def gen_test(a, b):
            def test(self):
                self.assertEqual(a, b)
            return test

        # create space
        for tname, a, b in l:
            test_name = "test_%s" % tname
            namespace[test_name] = gen_test(a,b)
        return type.__new__(mcs, name, bases, namespace)

_PY3 = sys.version_info >= (3, 0)

if _PY3:
    Meta = TestGenerator("Meta", (object,), {})
else:
    Meta = TestGenerator("Meta".encode("utf-8"), (object,), {})

class CompoundSequenceTests(Meta, unittest.TestCase):
    pass

#class CompoundSequenceTests(unittest.TestCase):
#
#    def setUp(self):
#        # Wrappers of list, set, tuple, dict, ...
#        # Slice, Range, Count, Cycle, Repeat
#        # Product, Permutations, Combinations, CombinationsR
#        # PermutationRange, CombinationRange
#            
#        # create pairs of (sgt, it)
#        # generate new test dynamically
#
#        # getitem, length, copy, deepcopy, +, index, in, iter, get
#        pass
#
#    def tearDown(self):
#        pass
#
#    def _iter_equals(self, iterable1, iterable2, N=True):
#
#        while N:
#            val = next(iterable1, None) 
#            ref = next(iterable2, None) 
#            if val is None and ref is None:
#                break
#            self.assertEqual(val, ref)
#            if N is not True:
#                N -= 1

test_classes = (CompoundSequenceTests,)

#
#import unittest
#
#l = [["foo", "a", "a",], ["bar", "a", "b"], ["lee", "b", "b"]]
#
#class TestSequenceMeta(type):
#    def __new__(mcs, name, bases, dict):
#
#        def gen_test(a, b):
#            def test(self):
#                self.assertEqual(a, b)
#            return test
#
#        for tname, a, b in l:
#            test_name = "test_%s" % tname
#            dict[test_name] = gen_test(a,b)
#        return type.__new__(mcs, name, bases, dict)
#
#class TestSequence(unittest.TestCase):
#    __metaclass__ = TestSequenceMeta
#
#if __name__ == '__main__':
#    unittest.main()
#
#Note: in python 3, change this to: class TestSequence(unittest.TestCase, metaclass=TestSequenceMeta):[...]
