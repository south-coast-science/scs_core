#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.specification.qualifier import Qualifier
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

Qualifier.load()

print("list...")
for qualifier in Qualifier.instances():
    print(qualifier)
print("-")

print("find...")
code = "BL"
qualifier = Qualifier.find(code)
print("code:%s qualifier:%s" % (code, qualifier))
print(JSONify.dumps(qualifier))
print("-")

code = "a"
qualifier = Qualifier.find(code)
print("code:%s qualifier:%s" % (code, qualifier))
print("-")

