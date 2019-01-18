# coding: utf-8

from __future__ import (unicode_literals, print_function,
        division)

import sys
import copy
import unittest

_PY3 = sys.version_info >= (3, 0)

def _prep(cls):
    # provide test utility functions
    # initialize test: namespace? setup, teardown, parameterized test?

    newbases = cls.__bases__ + (unittest.TestCase,)

    if _PY3:
        newcls = type('newcls', newbases, dict(cls.__dict__))
    else:
        newcls = type('newcls'.encode('utf-8'), newbases, dict(cls.__dict__))

    May use FunctionTestCase from unitest instead of creating new class?
    # TODO: may need different test runner
    newcls._testMethodName = 'runTest'

    for gname, gobj in globals().items():
        if gname.startswith("_assert"):
            setattr(newcls, gname[1:], gobj)

    return newcls

def _post(cls):
    # collect test result
    # forward test by-products

    import pdb; pdb.set_trace()

#     for key, val in cls.__dict__.items():
#         if key.startswith("__") and key.endswith("__") \ 
#                     or not callable(val):
#             continue
#         setattr(cls, key, trace(val))
#         print("Wrapped", key)
#     return cls


def testmethod(f):
    def funcwrap(obj, *vargs, **kwargs):
        clswrap = _prep(obj.__class__)
        f(clswrap, *vargs, **kwargs)
        return _post(clswrap)
    funcwrap.__doc__ = f.__doc__
    funcwrap.__name__ = f.__name__
    return funcwrap
