#!/usr/bin/env python3

"""
Created on 21 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_dict import CSVDict

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

# reference row...
jstr1 = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc_n2": {"pm1": 1, ' \
        '"bin1": {"1": 5, "2": 6}, "bin2": [[77, 88], {"my_key": "my_value"}]}}}'
print("jstr1: %s" % jstr1)
print("-")

# missing value...
jstr2 = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc_n2": {"pm1": 1, "pm2p5": 2, "pm10": 3, ' \
        '"bin1": {"1": 5, "2": 6}, "bin2": [7, 8], "mtf1": 9}}}'
print("jstr2: %s" % jstr2)
print("-")

# extra value...
jstr3 = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc_n2": {"pm1": 1, "pm2p5": 2, "pm10": 3, ' \
        '"per": 4, "xxx": 999, "bin1": {"1": 5, "2": 6}, "bin2": [7, 8], "mtf1": 9}}}'
print("jstr3: %s" % jstr3)
print("=")

# --------------------------------------------------------------------------------------------------------------------

datum = CSVDict.construct_from_jstr(jstr1)
print("datum: %s" % datum)
print("-")

header = datum.header
print("header: %s" % header)
print("-")

paths = header.paths()
print("paths: %s" % paths)
print("-")

# row = ["2016-09-27T13:29:52.947+01:00", 1, 5, 6, 77, 88, "my_value"]

row = datum.row(paths)
print("row: %s" % row)
print("-")

dictionary = header.as_dict(row)
print(dictionary)
print("-")

jstr = JSONify.dumps(dictionary)
print("jstr: %s" % jstr)
print("=")

'''
dictionary = datum.dictionary
print("dictionary: %s" % dictionary)
print("-")

jdict = CSVDict.as_dict(header, row)
print("as_dict: %s" % jdict)
print("-")

jstr = JSONify.dumps(jdict)
print("jstr: %s" % jstr)
print("=")
print("=")

# --------------------------------------------------------------------------------------------------------------------

jdict = json.loads(jstr2)
print("jdict2: %s" % jdict)
print("-")

datum = CSVDict.construct(jdict)
print("datum2: %s" % datum)
print("-")

row = datum.row(header)
print("row2: %s" % row)
print("-")

dictionary = datum.dictionary
print("dict2: %s" % dictionary)
print("-")

jdict = CSVDict.as_dict(header, row)
print("jdict2: %s" % jdict)
print("-")

jstr1 = JSONify.dumps(jdict)
print("jstr2: %s" % jstr1)
print("=")
print("=")

# --------------------------------------------------------------------------------------------------------------------

jdict = json.loads(jstr3)
print("jdict3: %s" % jdict)
print("-")

datum = CSVDict.construct(jdict)
print("datum3: %s" % datum)
print("-")

row = datum.row(header)
print("row3: %s" % row)
print("-")

dictionary = datum.dictionary
print("dict3: %s" % dictionary)
print("-")

jdict = CSVDict.as_dict(header, row)
print("jdict3: %s" % jdict)
print("-")

jstr1 = JSONify.dumps(jdict)
print("jstr3: %s" % jstr1)
print("=")
print("=")
'''

