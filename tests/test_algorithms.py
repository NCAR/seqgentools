
import unittest

import seqgentools as seq
import itertools as it

MAX = 100
DEBUG = False

def _fibo(n):
   if n <= 1:
       return n
   else:
       return(_fibo(n-1) + _fibo(n-2))

class AlgorithmTests(unittest.TestCase):

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
            try:
                self.assertEqual(val, ref)
            except:
                if DEBUG:
                    import pdb; pdb.set_trace()
                else:
                    reraise
            if N is not True:
                N -= 1

    def test_fibonacci_cache(self):

        fibo = seq.Fibonacci()
        for n in range(20):
            self.assertEqual(fibo[n], _fibo(n))

    def test_fibonacci_nocache(self):

        fibo = seq.Fibonacci(cache=None)
        for n in range(20):
            self.assertEqual(fibo[n], _fibo(n))

test_classes = (AlgorithmTests,)

