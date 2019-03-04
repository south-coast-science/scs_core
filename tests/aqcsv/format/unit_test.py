#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.format.unit import Unit


# --------------------------------------------------------------------------------------------------------------------

Unit.load()

print("list...")
for unit in Unit.units():
    print(unit)
print("-")

print("find...")
iso = "TUN"
code = CountryCode.find_by_iso(iso)
print("iso:%s code:%s" % (iso, code))
print("-")

iso = "TUX"
code = CountryCode.find_by_iso(iso)
print("iso:%s code:%s" % (iso, code))
print("-")

