#!/usr/bin/env python3

"""
Created on 27 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"tag": "scs-ap1-6", "rec": "2018-04-05T09:16:12.751+00:00", ' \
       '"val": {"CO": {"weV": 0.34863, "aeV": 0.268817, "weC": 0.064464, "cnc": 237.0}, ' \
       '"SO2": {"weV": 0.277004, "aeV": 0.276129, "weC": -0.000801, "cnc": 2.2}, ' \
       '"H2S": {"weV": 0.258504, "aeV": 0.222316, "weC": -0.091086, "cnc": 7.2}, ' \
       '"VOC": {"weV": 0.102127, "weC": 0.101793, "cnc": 1294.8}, ' \
       '"sht": {"hmd": 54.4, "tmp": 21.6}}}'

print(jstr)
print("-")


# --------------------------------------------------------------------------------------------------------------------

jdict = json.loads(jstr)

datum = PathDict(jdict)
print(datum)
print("=")


# --------------------------------------------------------------------------------------------------------------------

path = None
print("%s is path: %s is sub-path:%s" % (path, datum.has_path(path), datum.has_sub_path(path)))
leaves = datum.paths(path)
print("%s: %s" % (path, leaves))
print("-")

path = 'val'
print("%s is path: %s is sub-path:%s" % (path, datum.has_path(path), datum.has_sub_path(path)))
leaves = datum.paths(path)
print("%s: %s" % (path, leaves))
print("-")

path = 'val.CO'
print("%s is path: %s is sub-path:%s" % (path, datum.has_path(path), datum.has_sub_path(path)))
leaves = datum.paths(path)
print("%s: %s" % (path, leaves))
print("-")

path = 'val.CO.cnc'
print("%s is path: %s is sub-path:%s" % (path, datum.has_path(path), datum.has_sub_path(path)))
leaves = datum.paths(path)
print("%s: %s" % (path, leaves))
print("-")

path = 'val.CO.xxx'
print("%s is path: %s is sub-path:%s" % (path, datum.has_path(path), datum.has_sub_path(path)))
print("-")
