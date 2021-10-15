#!/usr/bin/env python3

"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.model.gas.vE.gas_request import GasRequest
from scs_core.sample.gases_sample import GasesSample


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"rec": "2021-10-15T09:14:38Z", "tag": "scs-be2-3", "ver": 1.0, "src": "AFE", ' \
       '"val": {"NO2": {"weV": 0.29, "aeV": 0.29557, "weC": 0.0005, "cnc": 17.9, "vCal": 12.799}, ' \
       '"Ox": {"weV": 0.39951, "aeV": 0.39988, "weC": 0.00196, "cnc": 54.6, "vCal": 1.795, "xCal": -0.392451}, ' \
       '"CO": {"weV": 0.37994, "aeV": 0.28975, "weC": 0.09457, "cnc": 409.5, "vCal": 380.414}, ' \
       '"sht": {"hmd": 58.6, "tmp": 22.3}}}'

sample = GasesSample.construct_from_jdict(json.loads(jstr))
print(sample)
print('-')

request = GasRequest(sample, -0.1, 0.2, 32.5)
print(request)
print('-')

print(JSONify.dumps(request))
