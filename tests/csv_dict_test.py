#!/usr/bin/env python3

'''
Created on 21 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

import json

from collections import OrderedDict

from scs_core.csv.csv_dict import CSVDict

from scs_core.common.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc": {"pm1": 5.1, "pm2p5": 22.7, "pm10": 195.1, "per": 5.0, "bin1": [77, 38, 52, 39, 9, 15, 9, 2], "bin2": [4, 1, 2, 4, 0, 0, 0, 0], "mtf1": 30, "mtf3": 34, "mtf5": 34, "mtf7": 39}}}'
print(jstr)
print("-")


# --------------------------------------------------------------------------------------------------------------------

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
print(jdict)
print("-")

datum = CSVDict(jdict)
print(datum)
print("-")

header = datum.header
print(header)
print("-")

row = datum.row
print(row)
print("-")

jdict = CSVDict.as_dict(header, row)
print(jdict)
print("-")

jstr = JSONify.dumps(jdict)
print(jstr)
print("=")


