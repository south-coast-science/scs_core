#!/usr/bin/env python3

"""
Created on 21 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime, ISO8601


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now()
print(now)
print("-")

iso = ISO8601.construct(now)
print(iso)
print("-")

print("date: %s" % iso.date)
print("time: %s" % iso.time)
print("time_secs: %s" % iso.time_secs)
print("time_millis: %s" % iso.time_millis)
print("timezone: %s" % iso.timezone)
