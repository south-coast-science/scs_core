#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.specification.qualifier import Qualifier
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

print("list...")
for qualifier in Qualifier.instances():
    print(qualifier)
print("-")

print("find...")
code = None
qualifier = Qualifier.instance(code)
print("code:%s qualifier:%s" % (code, qualifier))
print("-")

code = "BL"
qualifier = Qualifier.instance(code)
print("code:%s qualifier:%s" % (code, qualifier))

jdict = qualifier.as_json()
print(JSONify.dumps(qualifier))
print("-")

remade = Qualifier.construct_from_jdict(jdict)
print(remade)

equality = remade == qualifier
print("remade == qualifier: %s" % equality)
print("-")
