#!/usr/bin/env python3

"""
Created on 3 Mar 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://seattlecentral.edu/qelp/sets/057/057.html
"""

import json

from scs_core.data.json import JSONify
from scs_core.data.stats import Stats


# --------------------------------------------------------------------------------------------------------------------

with open('gaussian.json') as f:
    values = json.load(f)

# values = [1, 2, 3, 4, 5, 10]
precision = 3

stats = Stats.construct(values, prec=precision)
print(stats)

jstr = JSONify.dumps(stats)
print(jstr)
print("-")

stats = Stats.construct_from_jdict(json.loads(jstr))
print(stats)

jstr = JSONify.dumps(stats)
print(jstr)
print("-")

print("lower 3: %s" % stats.lower3)
print("lower 2: %s" % stats.lower2)
print("lower 1: %s" % stats.lower1)
print("-")

print("upper 1: %s" % stats.upper1)
print("upper 2: %s" % stats.upper2)
print("upper 3: %s" % stats.upper3)
