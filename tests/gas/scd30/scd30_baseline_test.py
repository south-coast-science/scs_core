#!/usr/bin/env python3

"""
Created on 2 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example output:
{"sn": {"calibrated-on": "2019-02-02T11:34:16Z", "offset": 50, "env": {"hmd": 66.0, "tmp": 11.0, "pA": 99.0}}}
"""

from scs_core.data.json import JSONify
from scs_core.data.datetime import LocalizedDatetime

from scs_core.gas.scd30.scd30_baseline import SCD30Baseline
from scs_core.gas.sensor_baseline import BaselineEnvironment, SensorBaseline

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

calibrated_on = LocalizedDatetime.construct_from_iso8601("2021-06-02T13:11:31+01:00")
offset = -123
environment = BaselineEnvironment(50.1, 23.4, 101.5)
print(environment)

baseline = SensorBaseline(calibrated_on, offset, environment)
print(baseline)

scd30_baseline = SCD30Baseline(baseline)
print(scd30_baseline)
print("-")

print(JSONify.dumps(scd30_baseline))
print("-")

scd30_baseline.save(Host)
scd30_baseline2 = SCD30Baseline.load(Host)
print(scd30_baseline2)

print(scd30_baseline2 == scd30_baseline)
