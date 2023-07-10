#!/usr/bin/env python3

"""
Created on 7 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.epochconverter.com
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.period import Period


# --------------------------------------------------------------------------------------------------------------------

start_time_str = '9:00'
end_time_str = '17:00'
timezone_str = 'America/New_York'

p1 = Period.construct(start_time_str, end_time_str, timezone_str)
print(p1)
print("-")

test = LocalizedDatetime.now()
print("test: %s" % test)
print("contained: %s" % str(test in p1))
