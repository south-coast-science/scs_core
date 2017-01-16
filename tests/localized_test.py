#!/usr/bin/env python3

'''
Created on 13 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------
# run...

loc = LocalizedDatetime.now()
print(loc)
print(loc.as_iso8601())
print("-")

loc = LocalizedDatetime.construct_from_iso8601(loc.as_iso8601())
print(loc)
print(loc.as_iso8601())
print("-")

loc = LocalizedDatetime.construct_from_iso8601(loc.as_iso8601())
print(loc)
