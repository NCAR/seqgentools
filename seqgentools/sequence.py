# coding: utf-8

from __future__ import unicode_literals, print_function, division

import sys
import abc
import copy
from math import ceil, factorial

PY3 = sys.version_info >= (3, 0)

if PY3:
    Object = abc.ABCMeta("Object", (object,), {})
    from functools import reduce
    long = int
else:
    Object = abc.ABCMeta("Object".encode("utf-8"), (object,), {})

INF = float("inf")
NAN = float("nan")

class InfinityError(Exception):
    pass

def _nPr(n, r):
    return factorial(n) // factorial(n-r)

def _nCr(n, r):
    return factorial(n) // (factorial(r) * factorial(n-r))

def _nCRr(n, r):
    return factorial(n+r-1) // (factorial(r) * factorial(n-1))

class Sequence(Object):

    def __new__(cls, *vargs, **kwargs):

        obj = super(Sequence, cls).__new__(cls, *vargs, **kwargs)
        obj._iter_key = 0

        return obj

    @abc.abstractmethod
    def __init__(self, *vargs, **kwargs):
        pass

    @abc.abstractmethod
    def getitem(self, key):
        pass

    @abc.abstractmethod
    def copy(self, memo={}):
        pass

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        return self.copy(memo=memo)

    def __add__(self, other):
        return Chain(self, other)

    def __getitem__(self, key):

        if isinstance(key, slice):
            return Slice(self, key)
        else:
            key = self._validate_key(key)

            if key < self._len:
                return self.getitem(key)
            else:
                clsname = self.__class__.__name__
                raise IndexError("%s index out of range"%clsname)

    def index(self, val):
        raise NotImplementedError()

    def __len__(self):
        return self._len

    def __iter__(self):

        self._iter_key = 0
        return self

    def __next__(self):

        if self._len == INF or self._iter_key < self._len:
            val = self.getitem(self._iter_key)
            self._iter_key += 1
            return val
        else:
            raise StopIteration

    def next(self):
        return self.__next__()

    def get(self, key, *vargs):
        val = self.__getitem__(key)
        if val is not None:
            return val
        elif vargs:
            return vargs[0]
        else:
            return None

    def pop(self, idx=None):

        if idx is None:
            if self._len == INF:
                raise ValueError(
                    "Infinite sequence does not support pop method.")
            item = self._sequence[-1]
            self._sequence = self._sequence[:-1]
        elif isinstance(idx, int):
            item = self._sequence[idx]
            self._sequence = self._sequence[:idx] + self._sequence[idx+1:]
        else:
            raise TypeError("pop method requires integer index.")

        self._len -= 1

        return item
        
    def _validate_key(self, key):

        if not isinstance(key, (int, long)):
            raise TypeError("Key should be 'int' or 'long' type: %s"%type(key))

        if key < 0:
            if self._len == INF:
                raise TypeError("Negative key for infinite sequence: %d"%key)
            return self._len + key
        elif self._len != INF and key >= self._len:
            raise IndexError("index '%d' is out of bound"%key)

        return key

    def _validate_sequence(self, sequence):

        if isinstance(sequence, Sequence):
            return sequence
        elif hasattr(sequence, "__len__"):
            return Wrapper(sequence)
        else:
            clsname = sequence.__class__.__name__
            raise TypeError("'%s' does not support len() method."%clsname)

class Wrapper(Sequence):

    def __init__(self, iterable):

        self._sequence = tuple(iterable)
        self._len = len(self._sequence)

    def getitem(self, key):

        return self._sequence[key]
        
    def copy(self, memo={}):
        return Wrapper(copy.deepcopy(self._sequence, memo))

class Slice(Sequence):

    def __init__(self, sequence, slc):

        self._sequence = sequence

        self._start = 0 if slc.start is None else slc.start
        self._stop = len(self._sequence) if slc.stop is None else slc.stop
        self._step = 1 if slc.step is None else slc.step

        _len = float(self._stop - self._start) / float(self._step)
        self._len = int(ceil(_len)) if _len > 0 else 0

    def getitem(self, key):

        val = self._start + self._step * key
        if ((self._step > 0 and val < self._stop) or
                (self._step < 0 and val > self._stop)):
            return self._sequence[val]
        
    def copy(self, memo={}):
        slc = slice(self._start, self._stop, self._step)
        return Slice(copy.deepcopy(self._sequennce, memo), slc)


class Range(Sequence):

    def __init__(self, *vargs):

        if len(vargs) == 1:
            self._start, self._stop, self._step = 0, vargs[0], 1
        elif len(vargs) == 2:
            self._start, self._stop, self._step = vargs[0], vargs[1], 1
        elif len(vargs) == 3:
            self._start, self._stop, self._step = vargs[0], vargs[1], vargs[2]
        else:
            raise Exception("The number of arguments is not correct"
                            " for 'Range': " + str(vargs))

        if self._step == 0:
            raise ValueError("Range step argument must not be zero.")
        elif any(not isinstance(v, int) for v in(
                self._start, self._stop, self._step)):
            raise ValueError("Range arguments must be integer type.")

        _len = float(self._stop - self._start) / float(self._step)
        self._len = int(ceil(_len)) if _len > 0 else 0

    def getitem(self, key):

        val = self._start + self._step * key
        if ((self._step > 0 and val < self._stop) or
                (self._step < 0 and val > self._stop)):
            return val

    def copy(self, memo={}):
        return Range(self._start, self._stop, self._step)


class Count(Sequence):

    def __init__(self, start=0, step=1):

        if isinstance(start, int) and isinstance(step, int):
            self._start, self._step = start, step
        else:
            raise ValueError("Count arguments must be integer type.")

        self._len = INF

    def getitem(self, key):

        return self._start + self._step * key

    def copy(self, memo={}):
        return Count(self._start, self._step)


class Cycle(Sequence):
       
    def __init__(self, sequence):

        self._sequence = self._validate_sequence(sequence)

        if isinstance(self._sequence, Sequence):
            if len(self._sequence) == INF:
                clsname = sequence.__class__.__name__
                raise TypeError("Can not cycle infinite sequence: '%s'."%
                    clsname)
        else:
            clsname = sequence.__class__.__name__
            raise TypeError("'%s' does not support len() method."%clsname)

        self._len = INF
        self._sequence_len = len(self._sequence)

    def getitem(self, key):

        if self._sequence_len > 0:
            if key >= self._sequence_len:
                key = key % self._sequence_len

            return self._sequence[key]

    def copy(self, memo={}):
        return Cycle(copy.deepcopy(self._sequence, memo))


class Repeat(Sequence):

    def __init__(self, elem, times=None):

        self._elem = elem

        if isinstance(times, int) or times is None:
            self._times = times
        else:
            raise ValueError("Repeat times argument must be an"
                             " integer type or None.")

        if times is None:
            self._len = INF
        else:
            self._len = times
            
    def getitem(self, key):

        return self._elem

    def copy(self, memo={}):
        return Repeat(self._elem, times=self._times)


class Chain(Sequence):

    def __init__(self, *sequences):

        self._sequences = []
        for seq in sequences:
            seq = self._validate_sequence(seq)
            if len(seq) > 0:
                self._sequences.append(seq)

        self._sequence_lens = [len(seq) for seq in self._sequences]
        
        if any(_l == INF for _l in self._sequence_lens[:-1]):
            raise InfinityError("Infinity sequence can not be chained except the last.")

        if len(self._sequence_lens) > 0:
            if self._sequence_lens[-1] == INF:
                self._len = INF
            else:
                self._len = sum(self._sequence_lens)
        else:
            self._len = 0

    def getitem(self, key):

        accum_len = 0
        for _len, seq in zip(self._sequence_lens, self._sequences):
            if key >= accum_len and key < accum_len + _len:
                return seq[key - accum_len]
            accum_len += _len

    def copy(self, memo={}):

        seqs = [copy.deepcopy(s, memo) for s in self._sequences]
        return Chain(*seqs)


class Product(Sequence):

    def __init__(self, *sequences):

        self._pools = []
        for seq in sequences:
            self._pools.append(self._validate_sequence(seq))

        self._pools.reverse()
        self._pool_lens = [len(seq) for seq in self._pools]
        self._dimension = len(self._pools)

        if any(_l == INF for _l in self._pool_lens):
            raise InfinityError("Product does not support infinite sequence.")

        self._len = reduce(lambda x, y: x*y, self._pool_lens)

    def getitem(self, key):

        product = [None]*self._dimension
        for dim, (_len, seq) in enumerate(zip(self._pool_lens, self._pools)):
            product[self._dimension-dim-1] = seq[key % _len]
            key = key // _len

        return tuple(product)

    def copy(self, memo={}):

        seqs = [copy.deepcopy(s, memo) for s in self._sequences]
        return Product(*seqs)

class Permutations(Sequence):

    def __init__(self, sequence, r=None):

        self._sequence = self._validate_sequence(sequence)

        self._n = len(self._sequence)

        if self._n == INF:
            raise InfinityError("Permutation do not support infinite sequence.")

        self._r = self._n if r is None else r
        if self._r > self._n:
            self._len = 0
        else:
            self._len = _nPr(self._n, self._r)

    def _kth(self, k, l, r):

        if r == 0:
            return []
        else:
            inc = _nPr(len(l)-1, r-1)
            for idx in range(len(l)):
                if k < (idx+1)*inc:
                    return Chain([l[idx]], self._kth(k-inc*idx, l[:idx]+l[idx+1:], r-1))

    def getitem(self, key):

        return tuple(self._kth(key, self._sequence, self._r))

    def copy(self, memo={}):

        return Permutations(copy.deepcopy(self._sequence, memo), r=self._r)


class Combinations(Sequence):

    def __init__(self, sequence, r):

        self._sequence = self._validate_sequence(sequence)

        self._n = len(self._sequence)

        if self._n == INF:
            raise InfinityError("Combination do not support infinite sequence.")

        self._r = r

        if r > self._n:
            self._len = 0
        else:
            self._len = _nCr(self._n, self._r)

    def _kth(self, k, l, r):

        if r == 0:
            return []
        elif len(l) == r:
            return l
        else:
            i = _nCr(len(l)-1, r-1)
            if k < i:
                return Chain(l[0:1], self._kth(k, l[1:], r-1))
            else:
                return self._kth(k-i, l[1:], r)

    def getitem(self, key):

        return tuple(self._kth(key, self._sequence, self._r))

    def copy(self, memo={}):

        return Combinations(copy.deepcopy(self._sequence, memo), self._r)

class CombinationsR(Sequence):

    def __init__(self, sequence, r):

        self._sequence = self._validate_sequence(sequence)

        self._n = len(self._sequence)

        if self._n == INF:
            raise InfinityError("Combination do not support infinite sequence.")

        self._r = r

        self._len = _nCRr(self._n, self._r)

    def _kth(self, k, l, r):

        if r == 0:
            return []
        else:
            i = _nCRr(len(l), r-1)
            if k < i:
                return Chain(l[0:1], self._kth(k, l, r-1))
            else:
                return self._kth(k-i, l[1:], r)

    def getitem(self, key):

        return tuple(self._kth(key, self._sequence, self._r))

    def copy(self, memo={}):

        return CombinationsR(copy.deepcopy(self._sequence, memo), self._r)

class PermutationRange(Sequence):

    def __init__(self, sequence):

        self._sequence = self._validate_sequence(sequence)

        self._n = len(self._sequence)

        if self._n == INF:
            raise InfinityError("PermutationRange do not support infinite sequence.")

        sub_perms = []
        self._len = 0
        for r in range(self._n+1):
            perm = Permutations(self._sequence, r=r)
            sub_perms.append(perm)
        self._chain = Chain(*sub_perms)
        self._len = len(self._chain)

    def getitem(self, key):

        return self._chain[key]

    def copy(self, memo={}):

        return PermutationRange(copy.deepcopy(self._sequence, memo))

class CombinationRange(Sequence):

    def __init__(self, sequence):

        self._sequence = self._validate_sequence(sequence)

        self._n = len(self._sequence)

        if self._n == INF:
            raise InfinityError("CombinationRange do not support infinite sequence.")

        sub_combs = []
        self._len = 0
        for r in range(self._n+1):
            comb = Combinations(self._sequence, r=r)
            sub_combs.append(comb)
        self._chain = Chain(*sub_combs)
        self._len = len(self._chain)

    def getitem(self, key):

        return self._chain[key]

    def copy(self, memo={}):

        return CombinationRange(copy.deepcopy(self._sequence, memo))

