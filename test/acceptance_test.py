#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import csv
import unittest
import subprocess
import tempfile
import filecmp

import interpolator.interpolator as interp

d_project = os.path.dirname(__file__) + os.sep + ".." + os.sep 
d_data = d_project + "data" + os.sep

class TestInterpolation_Acceptance(unittest.TestCase):
    def test_provided_example(self):
        fn_output = d_data + os.sep + "output.txt"
        if os.path.exists(fn_output):
            os.remove(fn_output)

        fn_input = d_data + "input_test_data.csv" 
        # subprocess.call(["python3", "interpolator/interpolator.py", fn_input, fn_output], cwd=d_project)
        # use 'main' to more easily test on Windows
        interp.main(fn_input, fn_output)
        fn_exp = "data/interpolated_test_data.csv"

        self.assertTrue(os.path.exists(fn_output))
        self.assert_csv_values_equal(fn_exp, fn_output)


    def assert_csv_values_equal(self, fn_exp, fn_test):
        with open(fn_exp, 'r') as infile_exp, open(fn_test, 'r') as infile_test:
            reader_exp = csv.reader(infile_exp)
            reader_test = csv.reader(infile_test)
            rows_exp = [row for row in reader_exp]
            rows_test = [row for row in reader_test]
        self.assertEqual(len(rows_exp), len(rows_test))
        for r_exp, r_test in zip(rows_exp, rows_test):
            self.assertEqual(len(r_exp), len(r_test))
            for e, t in zip(r_exp, r_test):
                self.assertAlmostEqual(float(e), float(t))



if __name__ == '__main__':
    unittest.main()