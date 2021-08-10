#!/usr/bin/env python3

"""
Created on 31 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.gas.minimum import Minimum


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"rec": "2021-07-30T19:45:00Z", "val": {' \
       '"NO2": {"weV": 0.31812, "cnc": 57.0, "aeV": 0.28576, "weC": 0.00323}, ' \
       '"Ox": {"weV": 0.41573, "cnc": 24.4, "aeV": 0.40003, "weC": 0.00181}, ' \
       '"NO": {"weV": 0.3081, "cnc": 34.9, "aeV": 0.28073, "weC": 0.05806}, ' \
       '"CO": {"weV": 0.35202, "cnc": 339.8, "aeV": 0.2881, "weC": 0.06908}, ' \
       '"sht": {"hmd": 69.9, "tmp": 18.5}}, ' \
       '"tag": "scs-bgx-401", ' \
       '"exg": {"vB20": {"NO2": {"cnc": 14.4}}}}'

jdict = json.loads(jstr)
print(jdict)
print("-")

minimum = Minimum('val.CO.cnc', 0, 340, jdict)
print(minimum)
print("-")

print(JSONify.dumps(minimum))
print("-")

print(minimum.cmd_tokens({'CO': 300}))
