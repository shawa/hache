import unittest
from hache import hache

hache.CACHE_DIR = 'hache_test_cache'


class TestPositionalArgs(unittest.TestCase):
    def test_referential_transparency(self):
        @hache
        def f1(x):
            return x

        for _ in range(2):
            # second time is loaded from disk
            self.assertEqual('a', f1('a'))

    def test_referential_transparency_kwargs(self):
        @hache
        def f2(x, foo='bar'):
            return {x: foo}

        expected = {1: 'baz'}
        for _ in range(2):
            result = f2(1, 'baz')
            self.assertEqual(expected, result)

    def test_subsequent_call_with_different_arguments_correctly_handled(self):
        @hache
        def f3(x):
            return x

        # initialize in cache
        f3(1)
        f3(2)

        self.assertNotEqual(f3(1), f3(2))

    def test_argument_defaults_preserved(self):
        @hache
        def f4(x, foo='bar'):
            return {x: foo}

        expected = {1: 'bar'}
        for _ in range(2):
            result = f4(1)
            self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
