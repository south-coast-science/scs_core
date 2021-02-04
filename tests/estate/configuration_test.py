#!/usr/bin/env python3

"""
Created on 27 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.estate.configuration import Configuration

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

conf = '{"hostname": "scs-bbe-003", ' \
       '"afe-baseline": {"sn1": {"calibrated-on": null, "offset": 0, "env": null}, "sn2": {"calibrated-on": null, ' \
       '"offset": 0, "env": null}, "sn3": {"calibrated-on": null, "offset": 0, "env": null}, ' \
       '"sn4": {"calibrated-on": null, "offset": 0, "env": null}}, "afe-calib": {"serial_number": "27-000001", ' \
       '"type": "810-0023-02", "calibrated_on": "2016-11-01", "dispatched_on": null, "pt1000_v20": 1.0, ' \
       '"sn1": {"serial_number": "212060308", "sensor_type": "NO2A43F", "we_electronic_zero_mv": 309, ' \
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
       '"pcb_gain": 0.8, "we_sensitivity_mv_ppb": 1.425, "we_cross_sensitivity_no2_mv_ppb": "n/a"}}, ' \
       '"aws-api-auth": {"endpoint": "aws.southcoastscience.com", ' \
       '"api-key": "de92c5ff-b47a-4cc4-a04c-62d684d64a1f"}, ' \
       '"aws-client-auth": {"endpoint": "asrfh6e5j5ecz.iot.us-west-2.amazonaws.com", "client-id": "scs-bbe-003", ' \
       '"cert-id": "cd505d98bf"}, "aws-group-config": {"group-name": "scs-bbe-003-group", ' \
       '"time-initiated": "2021-01-29T11:52:25Z", "unix-group": 987, "ml": true}, ' \
       '"aws-project": {"location-path": "south-coast-science-dev/development/loc/1", ' \
       '"device-path": "south-coast-science-dev/development/device"}, ' \
       '"csv-logger-conf": {"root-path": "/srv/removable_data_storage", "delete-oldest": true, ' \
       '"write-interval": 0}, "display-conf": null, ' \
       '"gas-baseline": {"NO2": {"calibrated-on": "2021-01-19T13:42:55Z", "offset": -3, ' \
       '"env": {"hmd": 40.9, "tmp": 25.0, "pA": null}}}, ' \
       '"gas-model-conf": {"uds-path": "pipes/lambda-gas-model.uds", "model-interface": "vB", ' \
       '"resource-names": {"NO2": "/trained-models/no2-vB-2020q13/xgboost-model"}}, ' \
       '"gps-conf": {"model": "SAM8Q", "sample-interval": 10, "tally": 60, ' \
       '"report-file": "/tmp/southcoastscience/gps_report.json", "debug": false}, ' \
       '"interface-conf": {"model": "DFE"}, "greengrass-identity": null, ' \
       '"mpl115a2-calib": {"calibrated-on": "2020-11-15T11:29:23Z", "c25": 510}, ' \
       '"mpl115a2-conf": null, "mqtt-conf": {"inhibit-publishing": false, "report-file": null, "debug": false}, ' \
       '"ndir-conf": {"model": "t1f1", "tally": 1, "raw": false}, ' \
       '"opc-conf": {"model": "N3", "sample-period": 10, "restart-on-zeroes": false, "power-saving": false}, ' \
       '"pmx-model-conf": {"uds-path": "pipes/lambda-pmx-model.uds", "model-interface": "s1", ' \
       '"resource-names": {"pm1": "/trained-models/pm1-s1-2020h1/xgboost-model", ' \
       '"pm2p5": "/trained-models/pm2p5-s1-2020h1/xgboost-model", ' \
       '"pm10": "/trained-models/pm10-s1-2020h1/xgboost-model"}}, ' \
       '"psu-conf": {"model": "OsloV1", "batt-model": null, "ignore-threshold": false, "reporting-interval": 20, ' \
       '"report-file": "/tmp/southcoastscience/psu_status_report.json"}, ' \
       '"pt1000-calib": {"calibrated-on": "2017-08-15T11:21:45Z", "v20": 0.320208}, ' \
       '"scd30-conf": {"sample-interval": 5, "temp-offset": 0.0}, ' \
       '"schedule": {"scs-climate": {"interval": 10.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1}, ' \
       '"scs-particulates": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}}, ' \
       '"shared-secret": {"key": "pYL7B1JcgJ2gy6MP"}, "sht-conf": {"int": "0x45", "ext": "0x45"}, ' \
       '"system-id": {"vendor-id": "SCS", "model-id": "BE2", "model": "Alpha BB Eng", "config": "V2", ' \
       '"system-sn": 3}, "timezone-conf": {"set-on": "2021-01-29T12:51:37Z", "name": null}}'

# --------------------------------------------------------------------------------------------------------------------

conf1 = Configuration.load(Host)
print(conf1)
print("-")

conf1.save(Host)
conf1 = Configuration.load(Host)
print(conf1)
print("-")

jstr = JSONify.dumps(conf1, indent=4)

print(jstr)
print("===")

conf2 = Configuration.construct_from_jdict(json.loads(jstr))
print(conf2)
print("-")

jstr = JSONify.dumps(conf1, indent=4)

print(jstr)
print("-")

equals = conf1 == conf2

print("equals: %s" % equals)
