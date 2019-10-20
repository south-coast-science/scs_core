#!/usr/bin/env python3

"""
Created on 26 Oct 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

raw:
{"rec": "2018-10-26T09:32:56.720+00:00",
"val": {"CO": {"weV": 0.286129, "cnc": 241.3, "aeV": 0.254441, "weC": 0.038556},
"sht": {"hmd": 54.4, "tmp": 21.5},

"tag": "scs-be2-2"}

aggregate:
{"rec": "2018-10-26T09:00:00.000+00:00",
"val": {"CO": {"weV": 0.299527, "aeV": 0.259448, "weC": 0.057112, "cnc": 318.958236},
"sht": {"hmd": 52.513719, "tmp": 22.012196}}}

"""

import json

from scs_core.gas.a4.a4_datum import A4Datum
from scs_core.gas.a4.a4_temp_comp import A4TempComp

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib

from scs_core.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

calib_jstr = '{"serial_number": "27-000001", "type": "810-0023-02", "calibrated_on": "2016-11-01", ' \
        '"dispatched_on": null, "pt1000_v20": 1.0, ' \
        '"sn1": {"serial_number": "212060308", "sensor_type": "NOGA4", "we_electronic_zero_mv": 309, ' \
        '"we_sensor_zero_mv": 3, "we_total_zero_mv": 312, "ae_electronic_zero_mv": 308, "ae_sensor_zero_mv": 1, ' \
        '"ae_total_zero_mv": 309, "we_sensitivity_na_ppb": -0.264, "we_cross_sensitivity_no2_na_ppb": -0.264, ' \
        '"pcb_gain": -0.73, "we_sensitivity_mv_ppb": 0.192, "we_cross_sensitivity_no2_mv_ppb": 0.192}, ' \
        '"sn2": {"serial_number": "132950202", "sensor_type": "CO A4", "we_electronic_zero_mv": 249, ' \
        '"we_sensor_zero_mv": 62, "we_total_zero_mv": 311, "ae_electronic_zero_mv": 253, "ae_sensor_zero_mv": -1, ' \
        '"ae_total_zero_mv": 252, "we_sensitivity_na_ppb": 0.299, "we_cross_sensitivity_no2_na_ppb": "n/a", ' \
        '"pcb_gain": 0.8, "we_sensitivity_mv_ppb": 0.239, "we_cross_sensitivity_no2_mv_ppb": "n/a"}, ' \
        '"sn3": {"serial_number": "134060009", "sensor_type": "SO2A4", "we_electronic_zero_mv": 266, ' \
        '"we_sensor_zero_mv": -1, "we_total_zero_mv": 265, "ae_electronic_zero_mv": 263, "ae_sensor_zero_mv": 2, ' \
        '"ae_total_zero_mv": 265, "we_sensitivity_na_ppb": 0.444, "we_cross_sensitivity_no2_na_ppb": "n/a", ' \
        '"pcb_gain": 0.8, "we_sensitivity_mv_ppb": 0.355, "we_cross_sensitivity_no2_mv_ppb": "n/a"}, ' \
        '"sn4": {"serial_number": "133910023", "sensor_type": "H2SA4", "we_electronic_zero_mv": 245, ' \
        '"we_sensor_zero_mv": -12, "we_total_zero_mv": 233, "ae_electronic_zero_mv": 251, "ae_sensor_zero_mv": 13, ' \
        '"ae_total_zero_mv": 264, "we_sensitivity_na_ppb": 1.782, "we_cross_sensitivity_no2_na_ppb": "n/a", ' \
        '"pcb_gain": 0.8, "we_sensitivity_mv_ppb": 1.425, "we_cross_sensitivity_no2_mv_ppb": "n/a"}}'


baseline_jstr = '{"sn1": {"calibrated-on": "2017-09-27T07:44:01.259+00:00", "offset": 7}, ' \
                '"sn2": {"calibrated-on": "2018-08-18T08:22:56.318+00:00", "offset": 80}, ' \
                '"sn3": {"calibrated-on": "2018-08-18T08:24:25.599+00:00", "offset": 24}, ' \
                '"sn4": {"calibrated-on": "2018-08-18T08:28:53.212+00:00", "offset": 22}}'

calib = AFECalib.construct_from_jdict(json.loads(calib_jstr))
co_calib = calib.sensor_calib(1)
print(co_calib)

baseline = AFEBaseline.construct_from_jdict(json.loads(baseline_jstr))
co_baseline = baseline.sensor_baseline(1)
print(co_baseline)

tc = A4TempComp.find(Sensor.CODE_CO)
print(tc)

print("-")

# raw...
temp = 21.5
we_v = 0.286129
ae_v = 0.254441

co_a4 = A4Datum.construct(co_calib, co_baseline, tc, temp, we_v, ae_v)
print(co_a4)

# aggregate...
temp = 22.012196
we_v = 0.299527
ae_v = 0.259448

co_a4 = A4Datum.construct(co_calib, co_baseline, tc, temp, we_v, ae_v)
print(co_a4)
