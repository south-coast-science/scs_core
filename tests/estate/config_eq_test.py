#!/usr/bin/env python3

"""
Created on 14 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.estate.configuration import Configuration


# --------------------------------------------------------------------------------------------------------------------

with open('config1.json') as f:
    jstr_c1 = f.read()

with open('config2.json') as f:
    jstr_c2 = f.read()

with open('config3.json') as f:
    jstr_c3 = f.read()


# --------------------------------------------------------------------------------------------------------------------

c1 = Configuration.construct_from_jdict(json.loads(jstr_c1))
print(c1)
print("-")

c2 = Configuration.construct_from_jdict(json.loads(jstr_c2))
print(c2)
print("-")

c3 = Configuration.construct_from_jdict(json.loads(jstr_c3))
print(c3)
print("-")

eq12 = c1 == c2
print("eq12: %s" % eq12)

eq13 = c1 == c3
print("eq13: %s" % eq13)
print("-")

print(JSONify.dumps(c1.diff(c3), indent=4))
