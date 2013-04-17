import unittest

from memoize import memoize

class TestMemoize(unittest.TestCase):
    @memoize(version=1)
    def fib(self, x):
        if x <= 1:
            return x
        else:
            return self.fib(x-1) + self.fib(x-2)

    @memoize(version=1)
    def append(self, *args, **kwargs):
        """Toy function to test kwargs"""
        ret = kwargs.copy()
        for i in xrange(len(args)):
            ret[i] = args[i]

        return ret

    @memoize(version=1)
    def unhashable(self, a, b):
        return (a,b)

    def test_memoize(self):
        self.assertEqual(55, self.fib(10))

    def test_kwargs(self):
        expected = {0: 'a',
                    1: 'b',
                    'c' : 5,
                    'd' : 6}
        self.assertEqual(expected,
                         self.append('a', 'b', c=5, d=6))

    def test_unhashable(self):
        expected = ([3,4], 5)
        self.assertEqual(expected,
                         self.unhashable([3, 4], 5))


if __name__ == "__main__":
    unittest.main()
