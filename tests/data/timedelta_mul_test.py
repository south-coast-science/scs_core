#!/usr/bin/env python3

"""
Created on 30 Aug 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

td = Timedelta(minutes=4, seconds=5)
print("td: %s" % td)
print("total_seconds: %s" % td.total_seconds())
print("-")

prod1 = td * 2
print("prod1: %s" % prod1)
print("total_seconds: %s" % prod1.total_seconds())

prod2 = 2 * td
print("prod2: %s" % prod2)
print("total_seconds: %s" % prod2.total_seconds())

