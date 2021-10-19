#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import argparse


class Interpolator(object):
    def read_file(self, fn_input):
        """
        Load a file from CSV
        Args:
            fn_input - input filename
        Returns:
            None
        Post-condition:
            Data member self.data contains list of lists of input data with None
            representing 'nan'. Otherwise, raises an Exception, e, if file is incorrectly 
            formatted with srt(e) describing the error. 
        """
        if not os.path.exists(fn_input):
            raise Exception("ERROR: Input file does not exist: %s" % fn_input)
        with open(fn_input, 'r') as infile:
            reader = csv.reader(infile)
            self.data = []
            for row in reader:
                self.data.append([])
                for value in row:
                    if value == 'nan':
                        self.data[-1].append(None)
                    else:
                        try:
                            self.data[-1].append(float(value))
                        except:
                            raise Exception("ERROR: unexpected text in input file: '%s'" % str(value))


    def write_interpolated(self, fn_output):
        """
        Write the interpolated data to CSV
        Args:
            fn_output - output filename
        Returns:
            None
        Post-condition:
            Interpolated data is written to file. 
        """
        new_data = [[self._get_value(i, j) if value is None else value for j, value in enumerate(row)] for i, row in enumerate(self.data)]
        try:
            with open(fn_output, 'w') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(new_data)
        except OSError:
            raise Exception("ERROR: Cannot write to output file: %s" % fn_output)


    
    def _get_value(self, i, j):
        """
        Get (i,j)-th value if present otherwise average
        Args:
            data - n x m list of lists of numbers/None
            i - outer index in [0,n)
            j - inner index in [0,m)
        Returns:
            x - the value to use for the (i,j)-th entry or None if (i,j) invalid
        """
        m = len(self.data)
        n = len(self.data[0])
        if i >= m or j >= n:
            return None
        if self.data[i][j] is None:
            indices = [(i+di, j+dj) for di, dj in [[0, -1], [0,1], [-1,0], [1,0]]]
            values = [self.data[x][y] for x,y in indices if 0<=x<m and 0<=y<n]
            if any(v is None for v in values):
                raise Exception("ERROR: Input contains adjacent missing values")
            return sum(values)/float(len(values))
        else:
            return self.data[i][j]


def main(fn_input, fn_output):
    """
    Interpolate values in csv file
    Args:
        fn_input - filename for input CSV file
        fn_output - filename for output CSV file
    Returns:
        None
    """
    # read file
    inter = Interpolator()
    inter.read_file(fn_input)
    inter.write_interpolated(fn_output)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Interpolate 'nan' values in a CSV file.")
        parser.add_argument("input", help="Input CSV filename")
        parser.add_argument("output", help="Input CSV filename")
        args = parser.parse_args()
        main(args.input, args.output)
    except Exception as e:
        print(str(e))
        print("Exiting...")
        sys.exit(1)