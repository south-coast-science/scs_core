#!/usr/bin/env python3

"""
Created on 3 Mar 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.data.stats import Stats


# --------------------------------------------------------------------------------------------------------------------

values = [1, 2, 3, 4, 5, 10]
precision = 6

stats = Stats.construct(values, prec=precision)
print(stats)

jstr = JSONify.dumps(stats)
print(jstr)
print("-")

stats = Stats.construct_from_jdict(json.loads(jstr))
print(stats)

jstr = JSONify.dumps(stats)
print(jstr)
