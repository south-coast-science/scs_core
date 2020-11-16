#!/usr/bin/env python3

"""
Created on 16 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.sample.particulates_sample import ParticulatesSample


# --------------------------------------------------------------------------------------------------------------------
# run...

jstr = '{"tag": "scs-be2-3", "src": "N3", "rec": "2019-12-10T15:24:04Z", ' \
       '"val": {"per": 4.9, "pm1": 5.6, "pm2p5": 6.7, "pm10": 6.8, ' \
       '"bin": [338, 42, 4, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ' \
       '"mtf1": 83, "mtf3": 101, "mtf5": 0, "mtf7": 0, "sfr": 0.61, ' \
       '"sht": {"hmd": 32.1, "tmp": 30.7}}}'

print(jstr)
print("-")

jdict = json.loads(jstr)

sample = ParticulatesSample.construct_from_jdict(jdict)
print(sample)
print("-")

print(JSONify.dumps(sample))

