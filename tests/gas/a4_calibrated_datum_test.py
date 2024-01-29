#!/usr/bin/env python3

"""
Created on 9 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example output:
{"weV": 0.40963, "aeV": 0.40126, "weC": 0.01729, "cnc": 43.7, "calV": 13.56061, "calXV": 0.00386}
"""

import json

from scs_core.data.json import JSONify
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.path_dict import PathDict

from scs_core.gas.a4.a4_calibrated_datum import A4Calibrator
from scs_core.gas.a4.a4_datum import A4Datum

from scs_core.gas.afe_calib import AFECalib


# --------------------------------------------------------------------------------------------------------------------

with open('/Users/bruno/SCS/conf/afe_calib-bgx-508-26-000208.json') as f:
    calib_jstr = f.read()

calib = AFECalib.construct_from_jdict(json.loads(calib_jstr))
print("calib: %s" % calib)
print("-")

sensor_calibs = calib.sensor_calibs()
print("sensor_calibs: %s" % sensor_calibs)
print("-")

no2_calib = sensor_calibs['NO2']
print("no2_calib: %s" % no2_calib)
print("-")

ox_calib = sensor_calibs['Ox']
print("ox_calib: %s" % ox_calib)
print("=")


# --------------------------------------------------------------------------------------------------------------------

era_start = LocalizedDatetime.construct_from_iso8601('2020-01-01T00:00:00Z')
print("era_start: %s" % era_start.as_iso8601())

era_end = LocalizedDatetime.construct_from_iso8601('2020-10-01T00:00:00Z')
print("era_end: %s" % era_end.as_iso8601())
print("=")


# --------------------------------------------------------------------------------------------------------------------

datum_jstr = '{"tag": "scs-bgx-508", "rec": "2020-12-09T13:04:29Z", "val": ' \
             '{"NO2": {"weV": 0.30338, "aeV": 0.27969, "weC": 2e-05, "cnc": 0.1}, ' \
             '"Ox": {"weV": 0.40963, "aeV": 0.40126, "weC": 0.01729, "cnc": 43.7}, ' \
             '"NO": {"weV": 0.2805, "aeV": 0.29094, "weC": -0.01024, "cnc": -26.2}, ' \
             '"SO2": {"weV": 0.27875, "aeV": 0.286, "weC": -0.01085, "cnc": -35.7}, ' \
             '"sht": {"hmd": 70.4, "tmp": 9.2}}}'

sample_datum = PathDict.construct_from_jstr(datum_jstr)
print(sample_datum)
print("-")

no2_datum = A4Datum.construct_from_jdict(sample_datum.node('val.NO2'))
print("NO2: %s" % no2_datum)

ox_datum = A4Datum.construct_from_jdict(sample_datum.node('val.Ox'))
print("Ox: %s" % ox_datum)
print("=")


# --------------------------------------------------------------------------------------------------------------------

no2_calibrator = A4Calibrator(no2_calib)
# no2_calibrator = A4Calibrator.construct(no2_calib, era_start, era_end)
print("no2_calibrator: %s" % no2_calibrator)

ox_calibrator = A4Calibrator(ox_calib)
# ox_calibrator = A4Calibrator.construct(ox_calib, era_start, era_end)
print("ox_calibrator: %s" % ox_calibrator)
print("=")

# print("Training...")
# rec = LocalizedDatetime.construct_from_iso8601('2020-01-02T12:13:14Z')
#
# calibrated_datum = no2_calibrator.train(rec, no2_datum)
# print(calibrated_datum)
# print(JSONify.dumps(calibrated_datum))
# print("-")

print("NO2...")
no2_calibrated_datum = no2_calibrator.calibrate(no2_datum)
print("no2_calibrated_datum: %s" % no2_calibrated_datum)
print(JSONify.dumps(no2_calibrated_datum))
print("-")

print("O3...")
o3_calibrated_datum = ox_calibrator.calibrate(ox_datum)
print("o3_calibrated_datum: %s" % o3_calibrated_datum)
print(JSONify.dumps(o3_calibrated_datum))
