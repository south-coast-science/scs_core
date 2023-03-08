#!/usr/bin/env python3

"""
Created on 8 Mar 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.array_dict import ArrayDict
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

array_dict = ArrayDict()
print(array_dict)
print("-")


array_dict = ArrayDict([("a", 1), ("a", 2), ("b", 4)])
print(array_dict)
print("-")

array_dict.append("a", 3)
print(array_dict)
print("-")

jdict = array_dict.as_json()
print(jdict)
print("-")

jstr = JSONify.dumps(array_dict)
print(jstr)
print("-")

print("a in: %s" % str('a' in array_dict))
print("a: %s" % array_dict.get("a"))

print("c in: %s" % str('c' in array_dict))
print("c: %s" % array_dict.get("c"))
