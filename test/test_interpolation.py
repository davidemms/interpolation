#/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import tempfile
import unittest

from interpolation import interpolation


# directory containing unittest data
d_data = os.path.basename(__file__) + os.sep + "test_data" + os.sep


class TestInterpolation(unittest.TestCase):
    def test_read_from_file_2x2(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # arrange
            fn = dir_test + os.sep + "data.csv"
            with open(fn, 'w') as outfile:
                outfile.write("7.5,9.1\n")
                outfile.write("3.2,1.5\n")
        
            # act
            data = interpolation.read_from_file(fn)

        # assert
        self.assertEqual(2, len(data))
        self.assertListEqual([7.5, 9.1], data[0])
        self.assertListEqual([3.2, 1.5], data[1])


    def test_read_from_file_3x3(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # arrange
            fn = dir_test + os.sep + "data.csv"
            with open(fn, 'w') as outfile:
                outfile.write("1,2,3\n")
                outfile.write("4,5,6\n")
                outfile.write("7,8,9\n")
        
            # act
            data = interpolation.read_from_file(fn)

        # assert
        self.assertEqual(3, len(data))
        self.assertListEqual([1.0, 2.0, 3.0], data[0])
        self.assertListEqual([4.0, 5.0, 6.0], data[1])
        self.assertListEqual([7.0, 8.0, 9.0], data[2])


    def test_read_from_file_nan(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # arrange
            fn = dir_test + os.sep + "data.csv"
            with open(fn, 'w') as outfile:
                outfile.write("1,nan\n")
                outfile.write("nan,2\n")
                outfile.write("3,4\n")
        
            # act
            data = interpolation.read_from_file(fn)

        # assert
        self.assertEqual(3, len(data))
        self.assertListEqual([1., None], data[0])
        self.assertListEqual([None, 2.], data[1])
        self.assertListEqual([3., 4.], data[2])


    def test_read_from_file_format_error(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # arrange
            fn = dir_test + os.sep + "data.csv"
            with open(fn, 'w') as outfile:
                outfile.write("1,other\n")
                outfile.write("nan,2\n")
        
            # act
            with self.assertRaises(Exception) as context:
                interpolation.read_from_file(fn)

            self.assertTrue("ERROR: unexpected text in input file: 'other'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()