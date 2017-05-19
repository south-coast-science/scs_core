#!/usr/bin/env python3

"""
Created on 17 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import tzlocal

from scs_core.data.json import JSONify
from scs_core.data.rtc_datetime import RTCDatetime


# --------------------------------------------------------------------------------------------------------------------
# run...

print("direct...")
dt = RTCDatetime(17, 5, 18, 4, 13, 45, 59)
print(dt)
print("-")

jstr = dt.as_json()
print(jstr)
print("-")

print("from jstr...")
dt = RTCDatetime.construct_from_jstr(jstr)
print(dt)
print("-")

loc = dt.as_localized_datetime(tzlocal.get_localzone())
print(loc)

print(JSONify.dumps(loc))
print("-")

print("from localized_datetime...")
dt = RTCDatetime.construct_from_localized_datetime(loc)
print(dt)

print(JSONify.dumps(dt))
print("-")
