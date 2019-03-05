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

tzinfo = now.tzinfo
print("tzinfo: %s" % tzinfo)
print("-")

timezone = pytz.timezone('Europe/Athens')
print("timezone: %s" % timezone)

localised = now.localize(timezone)
print("localised: %s" % localised)
print("=")
print("")
print("")

print("AQCSVDatetime without zone...")
utc_aqcsv = AQCSVDatetime(now.datetime)
print("utc_aqcsv: %s" % utc_aqcsv)
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
print("=")
print("")
print("")

print("AQCSVDatetime with zone...")
local_aqcsv = AQCSVDatetime(localised.datetime, timezone)
print("local_aqcsv: %s" % local_aqcsv)
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


print("AQCSVDatetime with unreported zone...")
nrz_aqcsv = AQCSVDatetime(localised.datetime)
print("nrz_aqcsv: %s" % nrz_aqcsv)
print("-")

print("nrz_aqcsv localised: %s" % nrz_aqcsv.localised())
print("-")

jstr = JSONify.dumps(nrz_aqcsv).strip('"')
print(jstr)

nrz_aqcsv = AQCSVDatetime.construct_from_jstr(jstr)
print("nrz_aqcsv: %s" % nrz_aqcsv)
print("-")

jstr = JSONify.dumps(nrz_aqcsv).strip('"')
print(jstr)
print("=")
print("")
print("")

print("utc_aqcsv == local_aqcsv...")
equality = local_aqcsv == utc_aqcsv
print("equality: %s" % equality)
print("-")

print("utc_aqcsv == nrz_aqcsv...")
equality = utc_aqcsv == nrz_aqcsv
print("equality: %s" % equality)
print("-")
