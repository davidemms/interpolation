#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import argparse


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
    try:
        data = read_from_file(fn_input)
    except Exception as e:
        print(str(e))
        print("Exiting...")
        return

    # write & fill in missing values
    print("ERROR: Interpolation has not been implemented yet")


def read_from_file(fn_input):
    """
    Load a file from CSV
    Args:
        fn_input - input filename
    Returns:
        data - list of lists of floats/None for present/absent data
    """
    with open(fn_input, 'r') as infile:
        reader = csv.reader(infile)
        data = []
        for row in reader:
            data.append([])
            for value in row:
                if value == 'nan':
                    data[-1].append(None)
                else:
                    try:
                        data[-1].append(float(value))
                    except:
                        raise Exception("ERROR: unexpected text in input file: '%s'" % str(value))
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpolate 'nan' values in a CSV file.")
    parser.add_argument("input", help="Input CSV filename")
    parser.add_argument("output", help="Input CSV filename")
    args = parser.parse_args()
    main(args.input, args.output)