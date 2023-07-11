#!/usr/bin/env python3

"""
Created on 7 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.epochconverter.com
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.diurnal_period import DiurnalPeriod


# --------------------------------------------------------------------------------------------------------------------

start_time_str = '9:00'
end_time_str = '17:00'
timezone_str = 'America/New_York'

p1 = DiurnalPeriod.construct(start_time_str, end_time_str, timezone_str)
print(p1)
print("-")

now = LocalizedDatetime.now()
print("now: %s" % now)
print("contained: %s" % str(now in p1))
print("-")

print("start: %s" % p1.start_datetime(now).utc())
print("end: %s" % p1.end_datetime(now).utc())
