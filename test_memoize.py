import unittest

from memoize import memoize

class TestMemoize(unittest.TestCase):
    @memoize(version=1)
    def fib(self, x):
        if x <= 1:
            return x
        else:
            return self.fib(x-1) + self.fib(x-2)
    def test_memoize(self):
        print self.fib(5)

if __name__ == "__main__":
    unittest.main()
