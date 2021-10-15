#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import argparse


def main(input, output):
    """
    Interpolate values in csv file
    Args:
        input - filename for input CSV file
        input - filename for output CSV file
    Returns:
        None
    """

def return2():
    return 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpolate 'nan' values in a CSV file.")
    parser.add_argument("input", help="Input CSV filename")
    parser.add_argument("output", help="Input CSV filename")
    args = parser.parse_args()
    main(args.input, args.output)