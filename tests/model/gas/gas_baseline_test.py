#!/usr/bin/env python3

"""
Created on 19 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.data.datetime import LocalizedDatetime

from scs_core.gas.sensor_baseline import SensorBaseline

from scs_core.model.gas.gas_baseline import GasBaseline


# --------------------------------------------------------------------------------------------------------------------

calibrated_on = LocalizedDatetime.construct_from_iso8601("2021-06-02T13:11:31+01:00")
sample_on = LocalizedDatetime.construct_from_iso8601("2021-06-01T13:11:31+01:00")
sample_humid = 54.3
sample_temp = 12.3

baseline1 = SensorBaseline(calibrated_on, sample_on, sample_humid, sample_temp, 1)
print(baseline1)

baseline2 = SensorBaseline(calibrated_on, sample_on, sample_humid, sample_temp, 2)
print(baseline1)
print("-")

baselines = GasBaseline({'NO2': baseline1, 'CO': baseline2})
print(baselines)
print("-")

jstr = JSONify.dumps(baselines)
print(jstr)
print("-")

baselines = GasBaseline.construct_from_jdict(json.loads(jstr))
print(baselines)
print("-")

offsets = baselines.offsets(gases=['CO', 'NO2', 'SO2'])
print(offsets)
