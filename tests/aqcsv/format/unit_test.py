#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.specification.unit import Unit
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

Unit.load()

print("list...")
for unit in Unit.instances():
    print(unit)
print("-")

print("find...")
code = "096"
unit = Unit.find(code)
print("code:%s unit:%s" % (code, unit))
print(JSONify.dumps(unit))
print("-")

code = "999"
unit = Unit.find(code)
print("code:%s unit:%s" % (code, unit))
print("-")

