#!/usr/bin/env python3

"""
Created on 28 Feb 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.sys.kernel import KernelSummary


# --------------------------------------------------------------------------------------------------------------------

summary1 = KernelSummary.construct()
print(summary1)

jstr = JSONify.dumps(summary1)
print(jstr)
print("-")

summary2 = KernelSummary.construct_from_jdict(json.loads(jstr))
print(summary2)

print("equal: %s" % str(summary1 == summary2))
