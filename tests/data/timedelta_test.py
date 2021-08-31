#!/usr/bin/env python3

"""
Created on 3 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Timedelta objects may or may not have a milliseconds component...
"""

from scs_core.data.json import JSONify
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

td = Timedelta(weeks=1, days=2, hours=3, minutes=4, seconds=5, milliseconds=6, microseconds=7)
print("td: %s" % td)
print("total_seconds: %s" % td.total_seconds())

jdict = td.as_json()
print("jdict: %s" % jdict)

print("jstr: %s" % JSONify.dumps(td))
print("-")

td = Timedelta.construct_from_jdict(jdict)
print("reconstructed: %s" % td)

print("=")

td = Timedelta(weeks=1, days=2, hours=3, minutes=4, seconds=5)
print("td: %s" % td)
print("total_seconds: %s" % td.total_seconds())

jdict = td.as_json()
print("jdict: %s" % jdict)

print("jstr: %s" % JSONify.dumps(td))
print("-")

td = Timedelta.construct_from_jdict(jdict)
print("reconstructed: %s" % td)

print("=")

