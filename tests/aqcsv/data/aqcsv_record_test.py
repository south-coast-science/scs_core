#!/usr/bin/env python3

"""
Created on 5 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aqcsv.data.aqcsv_record import AQCSVRecord, AQCSVFirstRecord, AQCSVSubsequentRecord
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

record1 = AQCSVRecord(site_code='124MM456789123', data_status=2, action_code=3,
                      datetime_code='20081008T1800-0600', parameter_code=42601, duration=6,
                      frequency=7, value=8, unit_code=9, qc_code=0, poc=11,
                      lat=12, lon=13, gis_datum=14, elev=15, method_code=90,
                      mpc_code=777, mpc_value=18, uncertainty=19, qualifiers=20)

print("AQCSVRecord...")
print("record1: %s" % record1)
print("-")

print("site: %s" % record1.site())
print("-")

print("datetime: %s" % record1.datetime())
print("-")

print("parameter: %s" % record1.parameter())
print("-")

print("unit: %s" % record1.unit())
print("-")

print("qc: %s" % record1.qc())
print("-")

print("method: %s" % record1.method())
print("-")

print("mpc: %s" % record1.mpc())
print("=")

jstr = JSONify.dumps(record1)
print(jstr)
print("-")

jdict = json.loads(jstr)

record2 = AQCSVRecord.construct_from_jdict(jdict)
print("record2: %s" % record2)
print("-")


equality = record1 == record2

print("record1 == record2: %s" % equality)
print("=")
print()

print("AQCSVFirstRecord...")
first1 = AQCSVFirstRecord('124456789123', 2, '20081008T1800', 42601, 5, 6, 7, 8, 9, 10, 11)
print("first1: %s" % first1)
print("-")

jstr = JSONify.dumps(first1)
print(jstr)
print("-")

first2 = AQCSVFirstRecord('124456789123', 2, '20081008T1800', 42601, 5, 6, 7, 8, 9, 10, 11)
print("first2: %s" % first2)
print("-")

equality = first1 == first2

print("first1 == first2: %s" % equality)
print("=")
print()

print("AQCSVSubsequentRecord...")
subsequent = AQCSVSubsequentRecord('124MM456789123', 2, '20081008T1800', 42601, 5, 6, 7, 8, 9)
print("subsequent: %s" % subsequent)
print("-")

jstr = JSONify.dumps(subsequent)
print(jstr)
print("-")
