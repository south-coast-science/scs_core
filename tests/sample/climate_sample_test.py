#!/usr/bin/env python3

"""
Created on 16 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.sample.climate_sample import ClimateSample


# --------------------------------------------------------------------------------------------------------------------
# run...

jstr = '{"tag": "scs-ap1-6", "rec": "2019-01-22T13:55:54Z", "val": {"hmd": 49.3, "tmp": 21.5, "bar": {"pA": 99.8}}}'
print(jstr)
print("-")

jdict = json.loads(jstr)

sample = ClimateSample.construct_from_jdict(jdict)
print(sample)
print("-")

print(JSONify.dumps(sample, sortable=True))

