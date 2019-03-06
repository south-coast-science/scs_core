#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.specification.unit import Unit
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

print("list...")
for unit in Unit.instances():
    print(unit)
print("-")

print("find...")
code = 999
unit = Unit.instance(code)
print("code:%s unit:%s" % (code, unit))
print("-")

code = 96
unit = Unit.instance(code)
print("code:%s unit:%s" % (code, unit))

jdict = unit.as_json()
print(JSONify.dumps(unit))
print("-")

remade = Unit.construct_from_jdict(jdict)
print(remade)

equality = remade == unit
print("remade == unit: %s" % equality)
print("-")
