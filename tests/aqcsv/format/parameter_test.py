#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.format.parameter import Parameter
from scs_core.aqcsv.format.unit import Unit

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------
parameter = None

Parameter.load()
Unit.load()

print("list...")
for parameter in Parameter.instances():
    print(parameter)
print("=")

print("check...")
for parameter in Parameter.instances():
    unit = parameter.unit

    if unit is None:
        print(parameter)
        print(unit)
        print("-")
print("=")

print("find...")
code = "88374"
parameter = Parameter.find(code)
print("iso:%s parameter:%s" % (code, parameter))
print(JSONify.dumps(parameter))
print("-")

code = "TUX"
parameter = Parameter.find(code)
print("iso:%s parameter:%s" % (code, parameter))
print("-")
