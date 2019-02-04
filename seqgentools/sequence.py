# coding: utf-8

from __future__ import (unicode_literals, print_function,
        division)

import sys
import abc
import copy
from math import ceil, factorial

_PY3 = sys.version_info >= (3, 0)

# TODO: support pop method

if _PY3:
    Object = abc.ABCMeta("Object", (object,), {})
    from functools import reduce
    long = int
else:
    Object = abc.ABCMeta("Object".encode("utf-8"),
            (object,), {})

INF = float("inf")
NAN = float("nan")

class InfiniteSequenceError(Exception):

    def __init__(self, obj):
        clsname = obj.__class__.__name__
        msg = "'%s' does not support infinite sequence."%clsname
        super(InfiniteSequenceError, self).__init__(msg)

class IndexNotFound(Exception):
    pass

def nPr(n, r):
    return factorial(n) // factorial(n-r)

def nCr(n, r):
    return factorial(n) // (factorial(r) * factorial(n-r))

def nCRr(n, r):
    return factorial(n+r-1) // (factorial(r) * factorial(n-1))

class Sequence(Object):

    def __new__(cls, *vargs, **kwargs):

        obj = super(Sequence, cls).__new__(cls)
        obj._iter_index = 0

        return obj

    @abc.abstractmethod
    def getitem(self, index):
        pass

    @abc.abstractmethod
    def length(self):
        pass

    @abc.abstractmethod
    def copy(self, memo={}):
        pass

    def __len__(self):
        return self.length()

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        return self.copy(memo=memo)

    def __add__(self, other):
        return Chain(self, other)

    def __getitem__(self, index):

        if isinstance(index, slice):
            return Slice(self, index)
        else:
            index = self._validate_index(index)

            if index < self.length():
                return self.getitem(index)
            else:
                clsname = self.__class__.__name__
                raise IndexError(
                        "Index is out of range at '%s'"%clsname)

    def index(self, val):
        clsname = self.__class__.__name__
        raise NotImplementedError(
            "'%s' does not support index() method."%clsname)

    def __contains__(self, val):
        try:
            idx = self.index(val)
            return True
        except NotImplementedError:
            clsname = self.__class__.__name__
            raise NotImplementedError(
                "'%s' does not support 'in' operation."%clsname)
        except IndexNotFound:
            return False

    def __iter__(self):

        self._iter_index = 0
        return self

    def __next__(self):

        if self.length() == INF or self._iter_index < self.length():
            val = self.getitem(self._iter_index)
            self._iter_index += 1
            return val
        else:
            raise StopIteration

    def next(self):
        return self.__next__()

    def get(self, index, *vargs):
        val = self.__getitem__(index)
        if val is not None:
            return val
        elif vargs:
            return vargs[0]
        else:
            return None

#    def pop(self, idx=None):
#
#        # TODO: fix a bug of self._sequence
#        if idx is None:
#            if self._len == INF:
#                raise ValueError(
#                    "Infinite sequence does not support pop method.")
#            if self._len == 0:
#                raise IndexError("pop from empty sequence")
#            item = self.__getitem__(-1)
#        elif isinstance(idx, int):
#            item = self.__getitem__(idx)
#            self._sequence = self._sequence[:idx] + self._sequence[idx+1:]
#        else:
#            raise TypeError("pop method requires integer index.")
#
#        if self._len != INF:
#            self._len -= 1
#
#        return item
        
    def _validate_index(self, index):

        if not isinstance(index, (int, long)):
            raise TypeError("Index should be 'int' or "
                "'long' type: %s"%type(index))

        _len = self.length()

        if index < 0:
            if _len == INF:
                raise TypeError("Infinite sequence does not support "
                    "negative index: %d"%index)
            return _len + index
        elif _len != INF and index >= _len:
            raise IndexError("Index '%d' is out of bound"%index)

        return index

    def _validate_sequence(self, sequence):

        if isinstance(sequence, Sequence):
            return sequence
        elif hasattr(sequence, "__len__"):
            return Wrapper(sequence)
        else:
            clsname = sequence.__class__.__name__
            raise TypeError("'%s' is not a valid sequenceable type."
                    %clsname)

class Wrapper(Sequence):

    def __init__(self, iterable):

        self._sequence = tuple(iterable)

    def getitem(self, index):

        return self._sequence[index]
        
    def copy(self, memo={}):
        return Wrapper(copy.deepcopy(self._sequence, memo))

    def length(self):
        return len(self._sequence)

class Slice(Sequence):

    def __init__(self, sequence, slc):

        self._sequence = self._validate_sequence(sequence)

        self._start = 0 if slc.start is None else slc.start
        self._stop = (self._sequence.length() if slc.stop is
                None else slc.stop)
        self._step = 1 if slc.step is None else slc.step

    def getitem(self, index):

        val = self._start + self._step * index
        if ((self._step > 0 and val < self._stop) or
                (self._step < 0 and val > self._stop)):
            return self._sequence[val]
        
    def copy(self, memo={}):
        slc = slice(self._start, self._stop, self._step)
        return Slice(copy.deepcopy(self._sequence, memo), slc)

    def length(self):
        _len = float(self._stop - self._start) / float(self._step)
        if _len == INF:
            return INF
        else:
            return int(ceil(_len)) if _len > 0 else 0

class Range(Sequence):

    def __init__(self, *vargs):

        if len(vargs) == 1 and type(vargs[0]) == type(range(1)):
            if hasattr(vargs[0], "stop"):
                s = vargs[0]
                self._start = 0 if s.start is None else s.start
                self._stop = INF if s.stop is None else s.stop
                self._step = 1 if s.step is None else s.step
            else:
                diff = vargs[0][1] - vargs[0][0]
                self._start, self._stop, self._step = (vargs[0][0],
                    vargs[0][-1]+diff, diff)
        else:
            s = slice(*vargs)
            self._start = 0 if s.start is None else s.start
            self._stop = sys.maxsize if s.stop is None else s.stop
            self._step = 1 if s.step is None else s.step

        if self._step == 0:
            raise ValueError("Range step argument must not be zero.")
        elif any(not isinstance(v, int) for v in(
                self._start, self._stop, self._step)):
            raise ValueError("Range arguments must be integer type.")

    def getitem(self, index):

        val = self._start + self._step * index
        if ((self._step > 0 and val < self._stop) or
                (self._step < 0 and val > self._stop)):
            return val

    def copy(self, memo={}):
        return Range(self._start, self._stop, self._step)

    def length(self):
        _len = float(self._stop - self._start) / float(self._step)
        if _len == INF:
            return INF
        else:
            return int(ceil(_len)) if _len > 0 else 0

class Count(Sequence):

    def __init__(self, start=0, step=1):

        if isinstance(start, int) and isinstance(step, int):
            self._start, self._step = start, step
        else:
            raise ValueError("Count arguments must be integer type.")

    def getitem(self, index):

        return self._start + self._step * index

    def copy(self, memo={}):
        return Count(self._start, self._step)

    def length(self):
        return INF

class Cycle(Sequence):
       
    def __init__(self, sequence):

        self._sequence = self._validate_sequence(sequence)

        if isinstance(self._sequence, Sequence):
            if self._sequence.length() == INF:
                clsname = sequence.__class__.__name__
                raise TypeError(
                    "Can not cycle infinite sequence: '%s'."%clsname)
        else:
            clsname = sequence.__class__.__name__
            raise TypeError(
                "'%s' does not support len() method."%clsname)

        self._sequence_len = self._sequence.length()

    def getitem(self, index):

        if self._sequence_len > 0:
            if index >= self._sequence_len:
                index = index % self._sequence_len

            return self._sequence[index]

    def copy(self, memo={}):

        return Cycle(copy.deepcopy(self._sequence, memo))

    def length(self):

        return INF

class Repeat(Sequence):

    def __init__(self, elem, times=None):

        self._elem = elem

        if times is None:
            self._times = INF
        elif isinstance(times, int) or times is None:
            self._times = times
        else:
            raise ValueError("Repeat times argument must be an"
                             " integer type or None.")
            
    def getitem(self, index):

        return self._elem

    def copy(self, memo={}):
        return Repeat(self._elem, times=self._times)

    def length(self):

        return self._times

class Chain(Sequence):

    def __init__(self, *sequences):

        self._sequences = []
        for seq in sequences:
            seq = self._validate_sequence(seq)
            if seq.length() > 0:
                self._sequences.append(seq)

        self._sequence_lens = [seq.length() for seq in self._sequences]
        
        if any(_l == INF for _l in self._sequence_lens[:-1]):
            raise InfiniteSequenceError(self)

    def getitem(self, index):

        accum_len = 0
        for _len, seq in zip(self._sequence_lens, self._sequences):
            if index >= accum_len and index < accum_len + _len:
                return seq[index - accum_len]
            accum_len += _len

    def copy(self, memo={}):

        seqs = [copy.deepcopy(s, memo) for s in self._sequences]
        return Chain(*seqs)

    def length(self):

        if len(self._sequence_lens) > 0:
            if self._sequence_lens[-1] == INF:
                return INF
            else:
                return sum(self._sequence_lens)
        else:
            return 0

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
