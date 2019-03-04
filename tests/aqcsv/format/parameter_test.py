#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.format.parameter import Parameter
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

Parameter.load()

print("list...")
for parameter in Parameter.parameters():
    print(parameter)
print("=")

print("check...")
for parameter in Parameter.parameters():
    unit = parameter.unit

    if unit is None:
        print(parameter)
        print(unit)
        print("-")
print("=")

print("find...")
code = "88374"
parameter = Parameter.find_by_code(code)
print("iso:%s code:%s" % (code, parameter))
print(JSONify.dumps(parameter))
print("-")

code = "TUX"
parameter = Parameter.find_by_code(code)
print("iso:%s code:%s" % (code, parameter))
print("-")
