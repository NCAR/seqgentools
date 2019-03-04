# coding: utf-8

from __future__ import (unicode_literals, print_function,
        division)

from math import factorial
import copy

from seqgentools.sequence import Sequence, Chain, INF

def nPr(n, r):
    return factorial(n) // factorial(n-r)

def nCr(n, r):
    return factorial(n) // (factorial(r) * factorial(n-r))

def nCRr(n, r):
    return factorial(n+r-1) // (factorial(r) * factorial(n-1))

class Product(Sequence):

    def __init__(self, *sequences, **kwargs):

        repeat = kwargs.pop("repeat", 1)

        self._pools = []
        for _ in range(repeat):
            for seq in sequences:
                self._pools.append(self._validate_sequence(seq))

        self._pools.reverse()
        self._pool_lens = [seq.length() for seq in self._pools]
        self._dimension = len(self._pools)

        if any(_l == INF for _l in self._pool_lens):
            raise InfiniteSequenceError(self)

    def getitem(self, index):

        product = [None]*self._dimension
        for dim, (_len, seq) in enumerate(zip(self._pool_lens,
                self._pools)):
            product[self._dimension-dim-1] = seq[index % _len]
            index = index // _len

        return tuple(product)

    def copy(self, memo={}):

        seqs = [copy.deepcopy(s, memo) for s in self._sequences]
        return Product(*seqs)

    def length(self):

        return reduce(lambda x, y: x*y, self._pool_lens)

class Permutations(Sequence):

    def __init__(self, sequence, r=None):

        self._sequence = self._validate_sequence(sequence)

        self._n = self._sequence.length()

        if self._n == INF:
            raise InfiniteSequenceError(self)

        self._r = self._n if r is None else r

    def _kth(self, k, l, r):

        if r == 0:
            return []
        else:
            inc = nPr(l.length()-1, r-1)
            for idx in range(l.length()):
                if k < (idx+1)*inc:
                    return Chain([l[idx]], self._kth(k-inc*idx,
                        l[:idx]+l[idx+1:], r-1))

    def getitem(self, index):

        return tuple(self._kth(index, self._sequence, self._r))

    def copy(self, memo={}):

        return Permutations(copy.deepcopy(self._sequence, memo),
                r=self._r)

    def length(self):

        if self._r > self._n:
            return 0
        else:
            return nPr(self._n, self._r)

class Combinations(Sequence):

    def __init__(self, sequence, r):

        self._sequence = self._validate_sequence(sequence)

        self._n = self._sequence.length()

        if self._n == INF:
            raise InfiniteSequenceError(self)

        self._r = r


    def _kth(self, k, l, r):

        if r == 0:
            return []
        elif l.length() == r:
            return l
        else:
            i = nCr(l.length()-1, r-1)
            if k < i:
                return Chain(l[0:1], self._kth(k, l[1:], r-1))
            else:
                return self._kth(k-i, l[1:], r)

    def getitem(self, index):

        return tuple(self._kth(index, self._sequence, self._r))

    def copy(self, memo={}):

        return Combinations(copy.deepcopy(self._sequence, memo),
                self._r)

    def length(self):

        if self._r > self._n:
            return 0
        else:
            return nCr(self._n, self._r)

class Combinations_with_replacement(Sequence):

    def __init__(self, sequence, r):

        self._sequence = self._validate_sequence(sequence)

        self._n = self._sequence.length()

        if self._n == INF:
            raise InfiniteSequenceError(self)

        self._r = r

    def _kth(self, k, l, r):

        if r == 0:
            return []
        else:
            i = nCRr(l.length(), r-1)
            if k < i:
                return Chain(l[0:1], self._kth(k, l, r-1))
            else:
                return self._kth(k-i, l[1:], r)

    def getitem(self, index):

        return tuple(self._kth(index, self._sequence, self._r))

    def copy(self, memo={}):

        return Combinations_with_replacement(copy.deepcopy(self._sequence, memo),
                self._r)

    def length(self):

        return nCRr(self._n, self._r)

class PermutationRange(Sequence):

    def __init__(self, sequence):

        self._sequence = self._validate_sequence(sequence)

        self._n = self._sequence.length()

        if self._n == INF:
            raise InfiniteSequenceError(self)

        sub_perms = []
        for r in range(self._n+1):
            perm = Permutations(self._sequence, r=r)
            sub_perms.append(perm)
        self._chain = Chain(*sub_perms)

    def getitem(self, index):

        return self._chain[index]

    def copy(self, memo={}):

        return PermutationRange(copy.deepcopy(self._sequence, memo))

    def length(self):

        return self._chain.length()

class CombinationRange(Sequence):

    def __init__(self, sequence):

        self._sequence = self._validate_sequence(sequence)

        self._n = self._sequence.length()

        if self._n == INF:
            raise InfiniteSequenceError(self)

        sub_combs = []
        for r in range(self._n+1):
            comb = Combinations(self._sequence, r=r)
            sub_combs.append(comb)
        self._chain = Chain(*sub_combs)

    def getitem(self, index):

        return self._chain[index]

    def copy(self, memo={}):

        return CombinationRange(copy.deepcopy(self._sequence, memo))

    def length(self):

        return self._chain.length()

class Fibonacci(Sequence):

    def __init__(self, cache_limit=1024):

        self._cache = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 5,
                       6: 8, 7: 13, 8: 21, 9: 34, 10: 55}
        self._cache_limit = None if cache is None else int(cache)

    def getitem(self, index):

        if not isinstance(index, int) or index < 0:
            raise ValueError("Invalid fibonacci index: %s."%str(index))

        if index in self._cache:
            return self._cache[index]

        kp, k, km = 1, 1, 0

        if self._cache_limit is not None:
            n = 1
            for bit in bin(index)[3:]:
                n *= 2
                if bit == '1':
                    n += 1

                    if n-1 in self._cache:
                        km = self._cache[n-1]
                    else:
                        km = (kp+km)*k
                        self._cache[n-1] = km

                    if n in self._cache:
                        k = self._cache[n]
                    else:
                        k = kp*kp+k*k
                        self._cache[n] = k

                    if n+1 in self._cache:
                        kp = self._cache[n+1]
                    else:
                        kp = k + km
                        self._cache[n+1] = kp
                else:
                    precalc = k*k

                    if n in self._cache:
                        k = self._cache[n]
                    else:
                        k = (kp+km)*k
                        self._cache[n] = k

                    if n-1 in self._cache:
                        km = self._cache[n-1]
                    else:
                        km = precalc+km*km
                        self._cache[n-1] = km

                    if n+1 in self._cache:
                        kp = self._cache[n+1]
                    else:
                        kp = kp*kp+precalc
                        self._cache[n+1] = kp

                if len(self._cache) > self._cache_limit-2:
                    self._cache_limit = None
        else:
            for bit in bin(index)[3:]:
                precalc = k*k
                kp, k, km = kp*kp+precalc, (kp+km)*k, precalc+km*km
                if bit == '1':
                    kp, k, km = kp+k, kp, k
        return k

    def copy(self, memo={}):

        return Fibonacci(cache_limit=self._cache_limit)

    def length(self):

        return INF
