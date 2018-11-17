#!/usr/bin/env python3

"""
Created on 6 Nov 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_writer import CSVWriter


# --------------------------------------------------------------------------------------------------------------------

# reference row...
jstr1 = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc_n2": {"pm1": 1, "pm2p5": 2, "pm10": 3, ' \
        '"per": 4, "bin1": {"a": 5, "b": 6}, "bin2": [7, 8], "mtf1": 9}}}'
print("jstr1: %s" % jstr1)
print("-")

# missing value...
jstr2 = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc_n2": {"pm1": 1, "pm2p5": 2, "pm10": 3, ' \
        '"bin1": {"a": 5, "b": 6}, "bin2": [7, 8], "mtf1": 9}}}'
print("jstr2: %s" % jstr2)
print("-")

# extra value...
jstr3 = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc_n2": {"pm1": 1, "pm2p5": 2, "pm10": 3, ' \
        '"per": 4, "xxx": 999, "bin1": {"a": 5, "b": 6}, "bin2": [7, 8], "mtf1": 9}}}'
print("jstr3: %s" % jstr3)
print("=")

# --------------------------------------------------------------------------------------------------------------------

writer = CSVWriter()
print(writer)
print("-")

writer.write(jstr1)
writer.write(jstr2)
writer.write(jstr3)
print("-")

print(writer)
