#!/usr/bin/env python3

"""
Created on 5 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.aqcsv.data.aqcsv_record import AQCSVRecord, AQCSVFirstRecord, AQCSVSubsequentRecord

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

record1 = AQCSVRecord(site=1, data_status=2, action_code=3, datetime_code='20081008T1800-0600', parameter=5,
                      duration=6, frequency=7, value=8, unit=9, qc=10,
                      poc=11, lat=12, lon=13, gis_datum=14, elev=15,
                      method_code=16, mpc=17, mpc_value=18, uncertainty=19, qualifiers=20)

print("record1: %s" % record1)
print("datetime: %s" % record1.datetime())
print("-")

jstr = JSONify.dumps(record1)
print(jstr)
print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)

record2 = AQCSVRecord.construct_from_jdict(jdict)
print("record2: %s" % record2)
print("-")


equality = record1 == record2

print("equals: %s" % equality)
print("=")


first1 = AQCSVFirstRecord(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
print("first1: %s" % first1)

first2 = AQCSVFirstRecord(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
print("first2: %s" % first2)
print("-")

equality = first1 == first2

print("equals: %s" % equality)
print("=")


subsequent = AQCSVSubsequentRecord(1, 2, 3, 4, 5, 6, 7, 8, 9)
print("subsequent: %s" % subsequent)
print("-")
