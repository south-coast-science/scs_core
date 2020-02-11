#!/usr/bin/env python3

"""
Created on 29 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.sys.uptime_datum import UptimeDatum


# --------------------------------------------------------------------------------------------------------------------
# run...

now = LocalizedDatetime.now()
print(now)
print("-")

report = "07:02:40 up 1 day,  0 users,  load average: 0.66, 0.65, 0.60"
print(report)
print("-")

uptime = UptimeDatum.construct_from_report(now, report)
print(uptime)
print("-")


report = "07:02:40 up 1 day, 19:34,  0 users,  load average: 0.66, 0.65, 0.60"
print(report)
print("-")

uptime = UptimeDatum.construct_from_report(now, report)
print(uptime)
print("-")


report = " 13:23:53 up 1 day, 33 min,  2 users,  load average: 0.01, 0.03, 0.01"
print(report)
print("-")

uptime = UptimeDatum.construct_from_report(now, report)
print(uptime)
print("-")


report = "9:31  up  1:09, 2 users, load averages: 0.82 0.96 1.00"
print(report)
print("-")

uptime = UptimeDatum.construct_from_report(now, report)
print(uptime)
print("-")


report = " 8:27  up 6 mins, 2 users, load averages: 3.78 2.20 1.09"
print(report)
print("-")

uptime = UptimeDatum.construct_from_report(now, report)
print(uptime)
print("=")

uptime = UptimeDatum.construct_from_report(now, report)
print(uptime)
print("-")

uptime = UptimeDatum.construct_from_report(now, report)
print(uptime)
print("-")

jstr = JSONify.dumps(uptime)
print(jstr)
print("-")

jdict = json.loads(jstr)
print(jdict)
print("-")

uptime = UptimeDatum.construct_from_jdict(jdict)
print(uptime)
print("-")

