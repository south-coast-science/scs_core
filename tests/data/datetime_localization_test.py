#!/usr/bin/env python3

"""
Created on 8 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from pytz import timezone

from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

zone = timezone("Europe/London")
print("zone: %s" % zone)
print("-")

summer = LocalizedDatetime.construct_from_iso8601("2023-08-08T15:10:13Z")
print("   summer: %s" % summer)

localised_summer = summer.localize(zone)
print("localised: %s" % localised_summer)
print("-")

winter = LocalizedDatetime.construct_from_iso8601("2023-01-08T15:10:13Z")
print("   winter: %s" % winter)

localised_winter = winter.localize(zone)
print("localised: %s" % localised_winter)
