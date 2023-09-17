#!/usr/bin/python3

import unittest

from chrisliz import factorial


class TestFctorial(unittest.TestCase):

    def test_factorial_with_positive_integer(self):
        self.assertEqual(factorial(5), 120)

    def test_factorial_with_zero(self):
        self.assertEqual(factorial(0), 1)

    def test_factorial_with_negative_integer(self):
        with self.assertRaises(ValueError):
            factorial(-1)


if __name__ == '__main__':
    unittest.main()
