#!/usr/bin/env python3

"""
Created on 13 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from datetime import date
from datetime import timedelta
from datetime import timezone

from pytz import timezone as pytz_timezone

from scs_core.data.datetime import DateParser, LocalizedDatetime


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
offset = 1 * timedelta(hours=2)
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

parser = DateParser.construct('YYYY-MM-DD')
print(parser)

airwatch_date = '2019-02-14'
airwatch_time = '24:00:00'

print("airwatch: %s %s" % (airwatch_date, airwatch_time))
loc = LocalizedDatetime.construct_from_date_time(parser, airwatch_date, airwatch_time)
print(loc)
print("-")

am_pm_date = '2019-10-01'
am_pm_time = '01:00 AM'

print("am/pm: %s %s" % (am_pm_date, am_pm_time))
loc = LocalizedDatetime.construct_from_date_time(parser, am_pm_date, am_pm_time)
print(loc)

print("construct_from_date...")
my_date = date(2021, month=1, day=2)
print(my_date)

loc = LocalizedDatetime.construct_from_date(my_date)
print(loc)

