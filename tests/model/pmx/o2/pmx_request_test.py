#!/usr/bin/env python3

"""
Created on 24 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.model.pmx.o2.pmx_request import PMxRequest

from scs_core.sample.climate_sample import ClimateSample
from scs_core.sample.particulates_sample import ParticulatesSample


# --------------------------------------------------------------------------------------------------------------------

pmx_jstr = '{"rec": "2024-01-24T14:32:35Z", "tag": "scs-be2-3", "ver": 2.0, "src": "N3", ' \
           '"val": {"per": 4.1, "pm1": 3.4, "pm2p5": 5.8, "pm10": 6.1, ' \
           '"bin": [276, 175, 80, 13, 11, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ' \
           '"mtf1": 27, "mtf3": 29, "mtf5": 40, "mtf7": 0, "sfr": 5.61, "sht": {"hmd": 42.6, "tmp": 23.8}}}'

pmx_sample = ParticulatesSample.construct_from_jdict(json.loads(pmx_jstr))
print(pmx_sample)
print("-")

climate_jstr = '{"rec": "2024-01-24T14:34:43Z", "tag": "scs-be2-3", "ver": 1.0, ' \
               '"val": {"hmd": 46.6, "tmp": 24.9, "bar": null}}'

climate_sample = ClimateSample.construct_from_jdict(json.loads(climate_jstr))
print(climate_sample)
print("-")

request = PMxRequest(climate_sample, pmx_sample, 0.1, 0.2, 0.3, 0.4)
print(request)
print('-')

print(JSONify.dumps(request))
