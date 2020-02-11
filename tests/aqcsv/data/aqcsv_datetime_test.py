#!/usr/bin/env python3

"""
Created on 5 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import pytz

from scs_core.aqcsv.data.aqcsv_datetime import AQCSVDatetime

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify


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
print("filename_prefix: %s" % utc_aqcsv.filename_prefix())
print("-")

print("utc_aqcsv localised: %s" % utc_aqcsv.localised())
print("-")

code = JSONify.dumps(utc_aqcsv).strip('"')
print(code)

utc_aqcsv = AQCSVDatetime.construct_from_code(code)
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
print("filename_prefix: %s" % local_aqcsv.filename_prefix())
print("-")

print("local_aqcsv localised: %s" % local_aqcsv.localised())
print("-")

code = JSONify.dumps(local_aqcsv).strip('"')
print(code)

local_aqcsv = AQCSVDatetime.construct_from_code(code)
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
print("filename_prefix: %s" % nrz_aqcsv.filename_prefix())
print("-")

print("nrz_aqcsv localised: %s" % nrz_aqcsv.localised())
print("-")

code = JSONify.dumps(nrz_aqcsv).strip('"')
print(code)

nrz_aqcsv = AQCSVDatetime.construct_from_code(code)
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
