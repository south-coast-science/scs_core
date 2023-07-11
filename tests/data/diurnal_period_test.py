#!/usr/bin/env python3

"""
Created on 7 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.epochconverter.com
"""

import json

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.diurnal_period import DiurnalPeriod
from scs_core.data.json import JSONify
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

start_time_str = '9:00'
end_time_str = '17:00'
timezone_str = 'Europe/London'

p1 = DiurnalPeriod.construct(start_time_str, end_time_str, timezone_str)
print(p1)
print("is_valid: %s" % p1.is_valid())
print("crosses_midnight: %s" % p1.crosses_midnight())
print("checkpoint: %s" % p1.checkpoint())

now = LocalizedDatetime.now()
print("has_expiring_dst: %s: %s" % (now.as_iso8601(), p1.has_expiring_dst()))

# go_back = LocalizedDatetime.construct_from_iso8601('2023-10-28T12:00:00Z')
# print("has_expiring_dst: %s: %s" % (go_back, p1.has_expiring_dst(go_back)))

print("-")

jstr = JSONify.dumps(p1)
print(jstr)
print("-")

p1 = DiurnalPeriod.construct_from_jdict(json.loads(jstr))
print(p1)
print("-")

start_time_str = '23:00'
end_time_str = '8:00'
timezone_str = 'Europe/London'

p2 = DiurnalPeriod.construct(start_time_str, end_time_str, timezone_str)
print(p2)
print("is_valid: %s" % p2.is_valid())
print("crosses_midnight: %s" % p2.crosses_midnight())
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
