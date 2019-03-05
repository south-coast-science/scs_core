#!/usr/bin/env python3

"""
Created on 5 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import pytz

from scs_core.aqcsv.data.aqcsv_datetime import AQCSVDatetime

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

print("LocalizedDatetime...")
now = LocalizedDatetime.construct_from_iso8601("2019-03-05T23:00:00.709+00:00")
print("now: %s" % now)
print("-")

datetime = now.datetime
print("datetime: %s" % datetime)
print("-")

timezone = pytz.timezone('Europe/Athens')
print("timezone: %s" % timezone)

localised = now.localize(timezone)
print("localised: %s" % localised)
print("=")
print("")
print("")

print("AQCSVDatetime with zone...")
local_aqcsv = AQCSVDatetime.construct_from_datetime(localised.datetime, timezone)
print("local_aqcsv: %s" % local_aqcsv)
print("is_utc: %s" % local_aqcsv.is_utc())
print("-")

print("local_aqcsv localised: %s" % local_aqcsv.localised())
print("-")

jstr = JSONify.dumps(local_aqcsv).strip('"')
print(jstr)

local_aqcsv = AQCSVDatetime.construct_from_jstr(jstr)
print("local_aqcsv: %s" % local_aqcsv)
print("-")

jstr = JSONify.dumps(local_aqcsv).strip('"')
print(jstr)
print("=")
print("")
print("")

print("AQCSVDatetime without zone...")
utc_aqcsv = AQCSVDatetime.construct_from_datetime(localised.datetime, None)
print("utc_aqcsv: %s" % utc_aqcsv)
print("is_utc: %s" % utc_aqcsv.is_utc())
print("-")

print("utc_aqcsv localised: %s" % utc_aqcsv.localised())
print("-")

jstr = JSONify.dumps(utc_aqcsv).strip('"')
print(jstr)

utc_aqcsv = AQCSVDatetime.construct_from_jstr(jstr)
print("utc_aqcsv: %s" % utc_aqcsv)
print("-")

jstr = JSONify.dumps(utc_aqcsv).strip('"')
print(jstr)
