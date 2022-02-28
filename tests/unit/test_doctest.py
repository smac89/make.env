import unittest
import doctest
import make_env


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, ignore=None):
    tests.addTests(doctest.DocTestSuite(make_env))
    return tests
