#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.specification.country import Country
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

Country.retrieve()

print("list...")
for country in Country.instances():
    print(country)
print("-")

print("find...")
iso = "TUN"
country = Country.instance(iso)
print("iso:%s country:%s" % (iso, country))
print(JSONify.dumps(country))
print("-")

numeric = country.numeric
country = Country.find_by_numeric(numeric)
print("numeric:%s country:%s" % (numeric, country))
print(JSONify.dumps(country))
print("-")

iso = "TUX"
country = Country.instance(iso)
print("iso:%s country:%s" % (iso, country))
print("-")
