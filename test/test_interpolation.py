#/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from interpolation import interpolation


class TestInterpolation(unittest.TestCase):
    def test_return2(self):
        self.assertEqual(interpolation.return2(), 2)



if __name__ == '__main__':
    unittest.main()