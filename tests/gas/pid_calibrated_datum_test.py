#!/usr/bin/env python3

"""
Created on 24 May 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example output:
{"weV": 0.40963, "aeV": 0.40126, "weC": 0.01729, "cnc": 43.7, "calV": 13.56061, "calXV": 0.00386}
"""

import json

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_core.gas.pid.pid_calibrated_datum import PIDCalibrator
from scs_core.gas.pid.pid_datum import PIDDatum

from scs_core.gas.afe_calib import AFECalib


# --------------------------------------------------------------------------------------------------------------------

with open('/home/scs/SCS/conf/afe_calib.json') as f:
    calib_jstr = f.read()

calib = AFECalib.construct_from_jdict(json.loads(calib_jstr))
print("calib: %s" % calib)
print("-")

sensor_calibs = calib.sensor_calibs()
print("sensor_calibs: %s" % {gas: str(sensor_calib) for gas, sensor_calib in sensor_calibs.items()})
print("-")

pid_calib = sensor_calibs['VOC']
print("pid_calib: %s" % pid_calib)
print("-")

# --------------------------------------------------------------------------------------------------------------------

datum_jstr = '{"rec": "2022-05-24T08:50:33Z", "tag": "scs-opc-1", "ver": 2.0, "src": "SD1", ' \
             '"val": {"VOC": {"weV": 0.0706, "weC": 0.07043, "cnc": 539.9}, "sht": {"hmd": 44.1, "tmp": 24.9}}}'

sample_datum = PathDict.construct_from_jstr(datum_jstr)
print(sample_datum)
print("-")

voc_datum = PIDDatum.construct_from_jdict(sample_datum.node('val.VOC'))
print("VOC: %s" % voc_datum)


# --------------------------------------------------------------------------------------------------------------------

pid_calibrator = PIDCalibrator(pid_calib)
print("pid_calibrator: %s" % pid_calibrator)
print("=")

print("VOC...")
voc_calibrated_datum = pid_calibrator.calibrate(voc_datum)
print("voc_calibrated_datum: %s" % voc_calibrated_datum)
print(JSONify.dumps(voc_calibrated_datum))
print("-")
