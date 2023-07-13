#!/usr/bin/env python3

"""
Created on 11 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import pytz

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now().localize(pytz.timezone('Europe/London'))
print("now: %s" % now)
print("daylight: %s" % now.dst())
print("-")

winter = (now - Timedelta(days=150)).localize(pytz.timezone('Europe/London'))
print("winter: %s" % winter)
print("daylight: %s" % winter.dst())
print("-")

print("difference: %s" % str(now.dst() - winter.dst()))
