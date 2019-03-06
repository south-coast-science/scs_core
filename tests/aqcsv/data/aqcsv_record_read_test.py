#!/usr/bin/env python3

"""
Created on 6 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aqcsv.data.aqcsv_record import AQCSVRecord
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

jstr1 = '{"site": 840060970004, "data_status": 0, "action_code": 10, "datetime": "20181122T0800-0800", ' \
       '"parameter": 88101, "duration": 60, "frequency": 0, "value": 2, "unit": 105, "qc": 0, "poc": 3, ' \
       '"lat": 38.403765, "lon": -122.818294, "GISDatum": "WGS84", "elev": 78, "method_code": 170, ' \
       '"mpc": 1, "mpc_value": 5, "uncertainty": "", "qualifiers": ""}'

print(jstr1)
print("-")

record = AQCSVRecord.construct_from_jdict(json.loads(jstr1))
print(record)
print("=")

print("site: %s" % record.site())
print("-")

print("datetime: %s" % record.datetime())
print("-")

print("parameter: %s" % record.parameter())
print("-")

print("unit: %s" % record.unit())
print("-")

print("qc: %s" % record.qc())
print("-")

print("method: %s" % record.method())
print("-")

print("mpc: %s" % record.mpc())
print("=")

jstr2 = JSONify.dumps(record)
print(jstr2)
print("-")

print("jstr1:%d jstr2:%d" % (len(jstr1.strip()), len(jstr2.strip())))

equality = jstr1.strip() == jstr2.strip()

print("jstr1 == jstr2: %s" % equality)

# for i in range(len(jstr1)):
#        print("%3d: %s %s" % (i, jstr1[i], jstr2[i]))
