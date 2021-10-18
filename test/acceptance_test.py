#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest
import subprocess
import tempfile
import filecmp


class TestInterpolation_Acceptance(unittest.TestCase):
    def test_provided_example(self):
        with tempfile.TemporaryDirectory() as dir_test:
            fn_output = dir_test + os.sep + "output.txt"
            subprocess.call(["python", "-m", "interpolator.interpolator", "data/input_test_data.csv", fn_output])
            fn_exp = "data/interpolated_test_data.csv"

            self.assertTrue(os.path.exists(fn_output))
            subprocess.call(["cat", fn_output])
            self.assertTrue(filecmp.cmp(fn_exp, fn_output))


if __name__ == '__main__':
    unittest.main()