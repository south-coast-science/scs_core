#!/usr/bin/env python3

"""
Created on 14 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.linear_regression import LinearRegression
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

j1 = '{"rec": "2016-10-14T14:19:15.677+01:00", "val": {"opc_n2": {"pm1": 1.5, "pm2p5": 2.7, "pm10": 3.3, ' \
     '"per": 5.0, "bin": [95, 30, 11, 1, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], ' \
     '"mtf1": 31, "mtf3": 29, "mtf5": 0, "mtf7": 0}}}'

j2 = '{"rec": "2016-10-14T14:19:20.680+01:00", "val": {"opc_n2": {"pm1": 1.8, "pm2p5": 4.3, "pm10": 6.9, ' \
     '"per": 5.0, "bin": [76, 36, 19, 6, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], ' \
     '"mtf1": 26, "mtf3": 35, "mtf5": 26, "mtf7": 35}}}'

j3 = '{"rec": "2016-10-14T14:19:25.680+01:00", "val": {"opc_n2": {"pm1": 0.9, "pm2p5": 1.7, "pm10": 22.4, ' \
     '"per": 5.0, "bin": [62, 23, 8, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0], ' \
     '"mtf1": 20, "mtf3": 24, "mtf5": 0, "mtf7": 0}}}'


# --------------------------------------------------------------------------------------------------------------------

lr = LinearRegression()
print(lr)
print("-")

d1 = PathDict.construct_from_jstr(j1)
print(d1)
print("-")

rec = LocalizedDatetime.construct_from_iso8601(d1.node('rec'))
val = d1.node('val.opc_n2.pm10')

lr.append(rec, val)
print(lr)
print("-")

d2 = PathDict.construct_from_jstr(j2)
print(d2)
print("-")

rec = LocalizedDatetime.construct_from_iso8601(d2.node('rec'))
val = d2.node('val.opc_n2.pm10')

lr.append(rec, val)
print(lr)
print("-")

d3 = PathDict.construct_from_jstr(j3)
print(d3)
print("-")

rec = LocalizedDatetime.construct_from_iso8601(d3.node('rec'))
val = d3.node('val.opc_n2.pm10')

lr.append(rec, val)
print(lr)
print("=")


# --------------------------------------------------------------------------------------------------------------------

rec, val = lr.midpoint()
print("midpoint - rec: %s val: %f" % (rec.as_iso8601(), val))
print("-")

