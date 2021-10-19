#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import csv
import tempfile
import unittest

import interpolator.interpolator as interp


class TestInterpolator(unittest.TestCase):
    def test_read_from_file_2x2(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # arrange
            fn = dir_test + os.sep + "data.csv"
            with open(fn, 'w', newline='') as outfile:
                outfile.write("7.5,9.1\n")
                outfile.write("3.2,1.5\n")
        
            # act
            x = interp.Interpolator()
            x.read_file(fn)

        # assert
        self.assertEqual(2, len(x.data))
        self.assertListEqual([7.5, 9.1], x.data[0])
        self.assertListEqual([3.2, 1.5], x.data[1])


    def test_read_from_file_3x3(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # arrange
            fn = dir_test + os.sep + "data.csv"
            with open(fn, 'w', newline='') as outfile:
                outfile.write("1,2,3\n")
                outfile.write("4,5,6\n")
                outfile.write("7,8,9\n")
        
            # act
            x = interp.Interpolator()
            x.read_file(fn)

        # assert
        data = x.data
        self.assertEqual(3, len(data))
        self.assertListEqual([1.0, 2.0, 3.0], data[0])
        self.assertListEqual([4.0, 5.0, 6.0], data[1])
        self.assertListEqual([7.0, 8.0, 9.0], data[2])


    def test_read_from_file_nan(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # arrange
            fn = dir_test + os.sep + "data.csv"
            with open(fn, 'w', newline='') as outfile:
                outfile.write("1,nan\n")
                outfile.write("nan,2\n")
                outfile.write("3,4\n")
        
            # act
            x = interp.Interpolator()
            x.read_file(fn)

        # assert
        data = x.data
        self.assertEqual(3, len(data))
        self.assertListEqual([1., None], data[0])
        self.assertListEqual([None, 2.], data[1])
        self.assertListEqual([3., 4.], data[2])


    def test_read_from_file_format_error(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # arrange
            fn = dir_test + os.sep + "data.csv"
            with open(fn, 'w', newline='') as outfile:
                outfile.write("1,other\n")
                outfile.write("nan,2\n")
        
            # act
            x = interp.Interpolator()
            with self.assertRaises(Exception) as context:
                x.read_file(fn)
            self.assertTrue("ERROR: unexpected text in input file: 'other'" in str(context.exception))


    def test_write_interpolated(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # read in some data
            fn = dir_test + os.sep + "data.csv"
            with open(fn, 'wt', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow([1,2,3])
                writer.writerow([4,'nan',6])
                writer.writerow([7,8,'nan'])
            x = interp.Interpolator()
            x.read_file(fn)

            # write 
            fn_out = dir_test + os.sep + "data.out.csv"
            x.write_interpolated(fn_out)

            # nan should be replaced with interpolated values
            with open(fn_out, 'r', newline='') as infile:
                self.assertEqual("1.0,2.0,3.0", next(infile).rstrip())
                self.assertEqual("4.0,5.0,6.0", next(infile).rstrip())
                self.assertEqual("7.0,8.0,7.0", next(infile).rstrip())
                # no more lines if file
                with self.assertRaises(StopIteration) as context:
                    next(infile)

    def test_write_interpolated_scientific_notation(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # read in some data
            fn = dir_test + os.sep + "data.csv"
            with open(fn, 'w', newline='') as outfile:
                outfile.write("1e7,20000,nan\n")
                outfile.write("4e7,nan,10000\n")
            x = interp.Interpolator()
            x.read_file(fn)

            fn_out = dir_test + os.sep + "data.out.csv"
            x.write_interpolated(fn_out)

            with open(fn_out, 'r', newline='') as infile:
                self.assertEqual("10000000.0,20000.0,15000.0", next(infile).rstrip())
                # precise formatting is not important, but test that values were read and 
                # calculated correctly
                self.assertEqual("40000000.0,13343333.333333334,10000.0", next(infile).rstrip())

    def test_write_interpolated_scientific_notation_in_and_out(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # read in some data
            fn = dir_test + os.sep + "data.csv"
            with open(fn, 'w', newline='') as outfile:
                outfile.write("1e20,nan,2e20\n")
            x = interp.Interpolator()
            x.read_file(fn)

            fn_out = dir_test + os.sep + "data.out.csv"
            x.write_interpolated(fn_out)

            with open(fn_out, 'r', newline='') as infile:
                # could read in again and check numeric values if precise formatting 
                # has any system dependencies. For now, just check values are correct, 
                # can improve flexibility of test if required.
                self.assertEqual("1e+20,1.5e+20,2e+20", next(infile).rstrip())
    
    def test_get_value_single_line(self):
        x = interp.Interpolator()
        x.data = [[1, None, -1],]
        self.assertEqual(1, x._get_value(0, 0))
        self.assertEqual(0, x._get_value(0, 1))
        self.assertEqual(-1, x._get_value(0, 2))

    
    def test_get_value_single_line_edge(self):
        x = interp.Interpolator()
        x.data = [[None, 5,]]
        self.assertEqual(5, x._get_value(0, 0))
    

    def test_get_value_corner(self):
        x = interp.Interpolator()
        x.data = [[1, 5, None], [1, 3, 4]]
        self.assertEqual(4.5, x._get_value(0, 2))
    

    def test_get_value_surrounded(self):
        x = interp.Interpolator()
        x.data = [[1, 2, 1], [10, None, 8], [1, 0, 3]]
        self.assertEqual(5.0, x._get_value(1, 1))
    

    def test_get_value_multiple_nan(self):
        x = interp.Interpolator()
        x.data = [[None, 2, 1], [10, None, 8], [1, 0, None]]
        self.assertEqual(6.0, x._get_value(0, 0))
        self.assertEqual(5.0, x._get_value(1, 1))
        self.assertEqual(4.0, x._get_value(2, 2))

        # test present values also
        self.assertEqual(2.0, x._get_value(0, 1))
        self.assertEqual(1.0, x._get_value(0, 2))
        self.assertEqual(10.0, x._get_value(1, 0))
        self.assertEqual(1.0, x._get_value(2, 0))


    def test_get_value_out_of_range(self):
        x = interp.Interpolator()
        x.data = [[1, 2, 1], [10, None, 8]]
        self.assertTrue(x._get_value(0, 3) is None)
        self.assertTrue(x._get_value(0, 2) is not None)
        self.assertTrue(x._get_value(1, 0) is not None)
        self.assertTrue(x._get_value(2, 0) is None)


    def test_get_value_adjacent_missing_values(self):
        x = interp.Interpolator()
        x.data = [[1, None, None],]
        self.assertEqual(1, x._get_value(0, 0))
        with self.assertRaises(Exception) as context:
            x._get_value(0, 1)
        with self.assertRaises(Exception) as context:
            x._get_value(0, 2)


    def test_handle_adjacent_missing_values(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # read in some data
            fn_input = dir_test + os.sep + "data.csv"
            with open(fn_input, 'w', newline='') as outfile:
                outfile.write("nan,nan,3\n")
            fn_output = dir_test + os.sep + "data.out.csv"
                
            with self.assertRaises(Exception) as context:
                interp.main(fn_input, fn_output)
            self.assertTrue("ERROR: Input contains adjacent missing values" in str(context.exception))


    def test_handle_missing_input(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # read in some data
            fn_input = dir_test + os.sep + "data.csv"
            fn_output = dir_test + os.sep + "data.out.csv"
        with self.assertRaises(Exception) as context:
            interp.main(fn_input, fn_output)
        self.assertTrue("ERROR: Input file does not exist" in str(context.exception))


    def test_handle_unwritable_output(self):
        with tempfile.TemporaryDirectory() as dir_test:
            # read in some data
            fn_input = dir_test + os.sep + "data.csv"
            fn_output = "/path/that/doesnt/exist/foo.txt"
            with open(fn_input, 'w', newline='') as outfile:
                outfile.write("1,2,3\n")
            with self.assertRaises(Exception) as context:
                interp.main(fn_input, fn_output)
            self.assertTrue("ERROR: Cannot write to output file" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
