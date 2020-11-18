#!/usr/bin/env python3

"""
Created on 16 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.sample.gases_sample import GasesSample


# --------------------------------------------------------------------------------------------------------------------
# run...

jstr = '{"tag": "scs-be2-3", "rec": "2020-11-16T13:46:43Z", ' \
       '"val": {"NO2": {"weV": 0.31407, "aeV": 0.30888, "weC": 0.00346, "cnc": 9.0}, ' \
       '"CO": {"weV": 0.33376, "aeV": 0.25232, "weC": 0.08404, "cnc": 351.6}, ' \
       '"SO2": {"weV": 0.26694, "aeV": 0.26644, "weC": -0.00482, "cnc": 14.4}, ' \
       '"VOC": {"weV": 0.07975, "weC": 0.07945, "cnc": 736.3}, ' \
       '"sht": {"hmd": 55.2, "tmp": 22.5}}, "exg": {"g1/2020q13": {"NO2": {"cnc": 1.2}}}}'

print(jstr)
print("-")

jdict = json.loads(jstr)

sample = GasesSample.construct_from_jdict(jdict)
print(sample)
print("-")

print(JSONify.dumps(sample))

