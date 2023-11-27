#!/usr/bin/env python3

"""
Created on 26 Nov 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_reader import CSVReader
from scs_core.csv.csv_writer import CSVWriter


# --------------------------------------------------------------------------------------------------------------------

reader = CSVReader.construct_for_file('source.csv')

# for row in reader.rows():
#     print(row)
print("-")

writer = CSVWriter(filename='output-no-blank-line.csv', append=True)
for row in reader.rows():
    writer.write(row)
print("-")

print(writer)
