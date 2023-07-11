#!/usr/bin/env python3

"""
Created on 10 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.diurnal_period import DiurnalPeriod


# --------------------------------------------------------------------------------------------------------------------

start_time_str = '9:00'
end_time_str = '19:30'
timezone_str = 'America/New_York'

p1 = DiurnalPeriod.construct(start_time_str, end_time_str, timezone_str)
print(p1)
print("-")

now = LocalizedDatetime.now()

print("start_datetime: %s" % p1.start_datetime(now))
print("end_datetime: %s" % p1.end_datetime(now))

cron = p1.cron(1)
print("cron: %s" % cron)

cron = p1.aws_cron(1)
print("aws_cron: %s" % cron)
