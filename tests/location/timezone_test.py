#!/usr/bin/env python3

"""
Created on 11 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from tzlocal import get_localzone

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.location.timezone import Timezone
from scs_core.location.timezone_conf import TimezoneConf


# --------------------------------------------------------------------------------------------------------------------

for zone_name in Timezone.zones():
    print(zone_name)

print("=")


zone_name = "Europe/London"               # Etc/UTC  US/Michigan  Europe/London   Asia/Calcutta
print("zone_name: %s" % zone_name)
print("valid: %s" % Timezone.is_valid(zone_name))

print("-")

now = LocalizedDatetime.now()

zone_conf = TimezoneConf(now, zone_name)
print(zone_conf)
print(JSONify.dumps(zone_conf))

print("-")

zone = zone_conf.timezone()
print(zone)
print(JSONify.dumps(zone))

print("-")

offset = zone.current_utc_offset()
print(offset)
print(JSONify.dumps(offset))

td = offset.as_timedelta()
print(td)

print("days: %d" % td.days)
print("hours: %d" % td.hours)
print("minutes: %d" % td.minutes)

print("-")

local_tz = get_localzone()
print(local_tz)

print("=")


offset = zone.utc_offset(2016, 12, 2, 1)
print(offset)
print(JSONify.dumps(offset))

td = offset.as_timedelta()
print(td)

print("-")

