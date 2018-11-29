#!/usr/bin/env python3

"""
Created on 29 Nov 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datum import Datum


# --------------------------------------------------------------------------------------------------------------------

value = None
precision = Datum.precision(value)
print("value:%s precision:%s" % (value, precision))
print("is_numeric:%s is_int:%s is_float:%s" % (Datum.is_numeric(value), Datum.is_int(value), Datum.is_float(value)))
print("-")

value = "hello"
precision = Datum.precision(value)
print("value:%s precision:%s" % (value, precision))
print("is_numeric:%s is_int:%s is_float:%s" % (Datum.is_numeric(value), Datum.is_int(value), Datum.is_float(value)))
print("-")

value = 1
precision = Datum.precision(value)
print("value:%s precision:%s" % (value, precision))
print("is_numeric:%s is_int:%s is_float:%s" % (Datum.is_numeric(value), Datum.is_int(value), Datum.is_float(value)))

if precision is not None:
    rounded = round(value, precision)
    print("rounded:%s" % rounded)
print("-")

value = 0x10
precision = Datum.precision(value)
print("value:%s precision:%s" % (value, precision))
print("is_numeric:%s is_int:%s is_float:%s" % (Datum.is_numeric(value), Datum.is_int(value), Datum.is_float(value)))
print("-")

value = 1.0
precision = Datum.precision(value)
print("value:%s precision:%s" % (value, precision))
print("is_numeric:%s is_int:%s is_float:%s" % (Datum.is_numeric(value), Datum.is_int(value), Datum.is_float(value)))

if precision is not None:
    rounded = round(value, precision)
    print("rounded:%s" % rounded)
print("-")

value = 1.5
precision = Datum.precision(value)
print("value:%s precision:%s" % (value, precision))
print("is_numeric:%s is_int:%s is_float:%s" % (Datum.is_numeric(value), Datum.is_int(value), Datum.is_float(value)))

if precision is not None:
    rounded = round(value, precision)
    print("rounded:%s" % rounded)
print("-")

value = "2."
precision = Datum.precision(value)
print("value:%s precision:%s" % (value, precision))
print("is_numeric:%s is_int:%s is_float:%s" % (Datum.is_numeric(value), Datum.is_int(value), Datum.is_float(value)))
print("-")

value = "2.4.5"
precision = Datum.precision(value)
print("value:%s precision:%s" % (value, precision))
print("is_numeric:%s is_int:%s is_float:%s" % (Datum.is_numeric(value), Datum.is_int(value), Datum.is_float(value)))
print("-")

value = 1.123
precision = Datum.precision(value)
print("value:%s precision:%s" % (value, precision))
print("is_numeric:%s is_int:%s is_float:%s" % (Datum.is_numeric(value), Datum.is_int(value), Datum.is_float(value)))
print("-")

value = 22.0 / 7.0
precision = Datum.precision(value)
print("value:%s precision:%s" % (value, precision))
print("is_numeric:%s is_int:%s is_float:%s" % (Datum.is_numeric(value), Datum.is_int(value), Datum.is_float(value)))
print("-")

rounded = round(value, precision)
print("rounded:%s" % rounded)

rounded = round(value)
print("rounded:%s" % rounded)
