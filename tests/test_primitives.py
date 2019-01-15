
import unittest

import seqgentools as sgt
import itertools as it

MAX = 100

class PrimitiveTests(unittest.TestCase):

    def setUp(self):
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

    def test_range(self):

        slc = (0, 0, 1) 
        self._iter_equals(iter(sgt.Range(*slc)), iter(range(*slc)))

        slc = (0, 1, 1) 
        self._iter_equals(iter(sgt.Range(*slc)), iter(range(*slc)))

        slc = (0, 10, 1) 
        self._iter_equals(iter(sgt.Range(*slc)), iter(range(*slc)))

        slc = (0, -10, -1) 
        self._iter_equals(iter(sgt.Range(*slc)), iter(range(*slc)))

    def test_count(self):

        slc = (0, 1) 
        self._iter_equals(iter(sgt.Count(*slc)), it.count(*slc), N=MAX)

        slc = (1, 1) 
        self._iter_equals(iter(sgt.Count(*slc)), it.count(*slc), N=MAX)

        slc = (-10, 1) 
        self._iter_equals(iter(sgt.Count(*slc)), it.count(*slc), N=MAX)

        slc = (0, -1) 
        self._iter_equals(iter(sgt.Count(*slc)), it.count(*slc), N=MAX)

    def test_cycle(self):

        iterable = range(5)
        self._iter_equals(iter(sgt.Cycle(iterable)), it.cycle(iterable), N=MAX)

        iterable = range(0)
        self._iter_equals(iter(sgt.Cycle(iterable)), it.cycle(iterable), N=MAX)

    def test_repeat(self):

        self._iter_equals(iter(sgt.Repeat(1)), it.repeat(1), N=MAX)


    def test_chain(self):

        iterables = (range(5), range(3))
        self._iter_equals(iter(sgt.Chain(*iterables)), it.chain(*iterables))

        slc = (0, 5, 1)
        iterables = (sgt.Range(*slc), range(3))
        self._iter_equals(iter(sgt.Chain(*iterables)), it.chain(*iterables))

        iterables = (sgt.Range(*slc), sgt.Range(*slc))
        self._iter_equals(iter(sgt.Chain(*iterables)), it.chain(*iterables))


    def test_product(self):

        iterables = (range(5), range(3))
        self._iter_equals(iter(sgt.Product(*iterables)), it.product(*iterables))

        slc = (0, 5, 1)

        iterables = (sgt.Range(*slc), range(3))
        self._iter_equals(iter(sgt.Product(*iterables)), it.product(*iterables))

        iterables = (sgt.Range(*slc), sgt.Chain(*(sgt.Range(*slc), sgt.Range(*slc))))
        self._iter_equals(iter(sgt.Chain(*iterables)), it.chain(*iterables))


    def test_permutations(self):

        l = range(5)
        for r in range(len(l)+1):
            sgtperm = iter(sgt.Permutations(l,r))
            itperm = it.permutations(l,r=r)
            self._iter_equals(sgtperm, itperm)

        self._iter_equals(iter(sgt.Permutations(l, r=2*len(l))), it.permutations(l, r=2*len(l)))

    def test_combinations(self):


        l = range(5)
        for r in range(len(l)+1):
            self._iter_equals(iter(sgt.Combinations(l,r)), it.combinations(l,r))
        self._iter_equals(iter(sgt.Combinations(l,len(l)*2)), it.combinations(l,len(l)*2))


    def test_permutationrange(self):

        l = range(5)

        perms = [it.permutations(l, r=r) for r in range(0, len(l)+1)]
        itpermrange = it.chain(*perms)
        sgtpermrange = iter(sgt.PermutationRange(l))

        self._iter_equals(sgtpermrange, itpermrange)

    def test_combinationrange(self):

        l = range(5)

        comb = [it.combinations(l, r=r) for r in range(0, len(l)+1)]
        combrange = it.chain(*comb)
        self._iter_equals(iter(sgt.CombinationRange(l)), combrange)


    def test_custom(self):

        loop1 = {"indvars": ('a', 'b', 'c')}
        loop2 = {"indvars": ('x', 'y', 'z')}
        loops = (loop1, loop2)

        xform1 = {"interchange": (1,2,3)}
        xform2 = {"unroll": (-1,-2,-3)}
        xforms = (xform1, xform2)
        search_space = (loops, xforms)

        search_generator = sgt.Product(*search_space)

        self.assertEqual(len(search_generator), 4)

test_classes = (PrimitiveTests,)

