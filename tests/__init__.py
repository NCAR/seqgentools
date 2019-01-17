import unittest

from .test_primitives import test_classes as primitive_tests
from .test_compounds import test_classes as compound_tests

def seqgentools_unittest_suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    all_tests = primitive_tests + compound_tests

    for test_class in all_tests:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    return suite
