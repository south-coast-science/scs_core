#!/usr/bin/env python3

"""
Created on 13 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from datetime import timedelta
from datetime import timezone

from pytz import timezone as pytz_timezone

from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------
# run...

print("now...")
now = LocalizedDatetime.now()
print(now)

iso = now.as_iso8601()
print(iso)
print("-")


print("from iso...")
loc = LocalizedDatetime.construct_from_iso8601(iso)
print(loc)

iso = loc.as_iso8601()
print(iso)
print("-")


print("from truncated iso...")
iso = "2017-05-18T10:42:50+00:00"
print("iso: %s" % iso)

loc = LocalizedDatetime.construct_from_iso8601(iso)
print(loc)
print("-")


print("from truncated iso z...")
iso = "2017-05-18T10:42:50Z"
print("iso: %s" % iso)

loc = LocalizedDatetime.construct_from_iso8601(iso)
print(loc)
print("-")


print("datetime localise...")
offset = 1 * timedelta(hours=2, minutes=0)
print("offset: %s" % offset)

zone = timezone(offset)
print("zone: %s" % zone)

loc = now.localize(zone)
print(loc)

iso = loc.as_iso8601()
print(iso)
print("-")


print("pytz localise...")
zone = pytz_timezone('US/Pacific')
print("zone: %s" % zone)

loc = now.localize(zone)
print(loc)

iso = loc.as_iso8601()
print(iso)
print("-")

