#!/usr/bin/env python3

"""
Created on 7 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.epochconverter.com
"""

import json

from scs_core.data.json import JSONify
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.period import Period
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

start_time_str = '9:00'
end_time_str = '17:00'
timezone_str = 'Europe/London'

p1 = Period.construct(start_time_str, end_time_str, timezone_str)
print(p1)
print("has_valid_start_end: %s" % p1.has_valid_start_end())
print("-")

jstr = JSONify.dumps(p1)
print(jstr)
print("-")

p1 = Period.construct_from_jdict(json.loads(jstr))
print(p1)
print("-")

start_time_str = '8:00'
end_time_str = '16:00'
timezone_str = 'Europe/London'

p2 = Period.construct(start_time_str, end_time_str, timezone_str)
print(p2)
print("-")

print(Str.collection(sorted([p2, p1])))
print("-")

test = LocalizedDatetime.construct_from_timestamp(1675760400)      # 2023-02-07 09:00:00+00:00
print("test: %s" % test)
print("contained: %s" % str(test in p1))
print("-")

test = LocalizedDatetime.construct_from_timestamp(1688716800)      # 2023-07-07 09:00:00+01:00
print("test: %s" % test)
print("contained: %s" % str(test in p1))
print("-")

test = LocalizedDatetime.construct_from_timestamp(1688745600)      # 2023-07-07 17:00:00+01:00
print("test: %s" % test)
print("contained: %s" % str(test in p1))
print("-")

test = LocalizedDatetime.now()
print("test: %s" % test)
print("contained: %s" % str(test in p1))
