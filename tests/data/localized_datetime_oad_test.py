#!/usr/bin/env python3

"""
Created on 26 Sep 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from pytz import timezone as pytz_timezone

from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------
# run...

oad = 43733.54461

print("oad: %f..." % oad)
datetime = LocalizedDatetime.construct_from_oad(oad)
print(datetime)
print("-")

timezone = pytz_timezone('Europe/Athens')
print("timezone: %s..." % timezone)

datetime = LocalizedDatetime.construct_from_oad(oad, timezone)
print(datetime)
print("-")

print("pulled to UTC...")
datetime = datetime.utc()
print(datetime)
print("-")

