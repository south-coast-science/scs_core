#!/usr/bin/env python3

"""
Created on 22 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_reader import CSVReader


# --------------------------------------------------------------------------------------------------------------------

reader = CSVReader.construct_for_file('test.csv')
print(reader)
print("=")

for datum in reader.rows():
    print(datum)
    print("-")

reader.close()

