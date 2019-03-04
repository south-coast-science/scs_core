#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.format.country import Country
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

Country.load()

print("list...")
for country in Country.instances():
    print(country)
print("-")

print("find...")
iso = "TUN"
country = Country.find(iso)
print("iso:%s country:%s" % (iso, country))
print(JSONify.dumps(country))
print("-")

iso = "TUX"
country = Country.find(iso)
print("iso:%s code:%s" % (iso, country))
print("-")
