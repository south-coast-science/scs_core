#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.format.country_code import CountryCode


# --------------------------------------------------------------------------------------------------------------------

CountryCode.load()

print("list...")
for code in CountryCode.codes():
    print(code)
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
