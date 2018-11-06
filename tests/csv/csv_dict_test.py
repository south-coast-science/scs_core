#!/usr/bin/env python3

"""
Created on 21 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.csv.csv_dict import CSVDict

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

# reference row...
jstr1 = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc": {"pm1": 1, "pm2p5": 2, "pm10": 3, ' \
        '"per": 4, "bin1": {"a": 5, "b": 6}, "bin2": [7, 8], "mtf1": 9}}}'
print("jstr1: %s" % jstr1)
print("-")

# missing value...
jstr2 = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc": {"pm1": 1, "pm2p5": 2, "pm10": 3, ' \
        '"bin1": {"a": 5, "b": 6}, "bin2": [7, 8], "mtf1": 9}}}'
print("jstr2: %s" % jstr2)
print("-")

# extra value...
jstr3 = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc": {"pm1": 1, "pm2p5": 2, "pm10": 3, ' \
        '"per": 4, "xxx": 999, "bin1": {"a": 5, "b": 6}, "bin2": [7, 8], "mtf1": 9}}}'
print("jstr3: %s" % jstr3)
print("=")
print("=")

# --------------------------------------------------------------------------------------------------------------------

jdict = json.loads(jstr1, object_pairs_hook=OrderedDict)
print("jdict1: %s" % jdict)
print("-")

datum = CSVDict.construct(jdict)
print("datum1: %s" % datum)
print("-")

header = datum.header
print("header: %s" % header)
print("-")

row = datum.row(header)
print("row1: %s" % row)
print("-")

dictionary = datum.dictionary
print("dict1: %s" % dictionary)
print("-")

jdict = CSVDict.as_dict(header, row)
print("jdict1: %s" % jdict)
print("-")

jstr1 = JSONify.dumps(jdict)
print("jstr1: %s" % jstr1)
print("=")
print("=")

# --------------------------------------------------------------------------------------------------------------------

jdict = json.loads(jstr2, object_pairs_hook=OrderedDict)
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

jdict = json.loads(jstr3, object_pairs_hook=OrderedDict)
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
