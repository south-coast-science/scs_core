#!/usr/bin/env python3

"""
Created on 13 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

./csv_writer_scan_test.py | csv_reader.py -n
"""

import sys

from scs_core.csv.csv_writer import CSVWriter


# --------------------------------------------------------------------------------------------------------------------

writer = CSVWriter(header_scan=True)

jstr = '{"b": {"x": 1}, "c": null, "d": 3, "f": 4}'
print("jstr: %s" % jstr, file=sys.stderr)
writer.write(jstr)
print(writer, file=sys.stderr)
print("-", file=sys.stderr)

jstr = '{"a": 1, "b": null, "c": {"x": 3}, "e": 4}'
print("jstr: %s" % jstr, file=sys.stderr)
writer.write(jstr)
print(writer, file=sys.stderr)
print("-", file=sys.stderr)

jstr = '{"a": 1, "b": null, "c": {"x": 3, "y": 4}, "e": 5}'
print("jstr: %s" % jstr, file=sys.stderr)
writer.write(jstr)
print(writer, file=sys.stderr)
print("-", file=sys.stderr)

writer.close()
