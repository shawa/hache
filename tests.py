import unittest
from shutil import rmtree
from os import mkdir
from hache import hache, CACHE_DIR


class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        rmtree(CACHE_DIR)
        mkdir(CACHE_DIR)

    def test_referential_transparency(self):
        @hache
        def f(x):
            return x

        for _ in range(2):
            # second time is loaded from disk
            self.assertEqual('a', f('a'))

    def test_referential_transparency_kwargs(self):
        @hache
        def f(x, foo='bar'):
            return {x: foo}

        expected = {1: 'baz'}
        for _ in range(2):
            result = f(1, 'baz')
            self.assertEqual(expected, result)

    def test_subsequent_call_with_different_arguments_correctly_handled(self):
        @hache
        def f(x):
            return x

        # initialize in cache
        f(1)
        f(2)

        self.assertNotEqual(f(1), f(2))

    def test_argument_defaults_preserved(self):
        @hache
        def f(x, foo='bar'):
            return {x: foo}

        expected = {1: 'bar'}
        for _ in range(2):
            result = f(1)
            self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
