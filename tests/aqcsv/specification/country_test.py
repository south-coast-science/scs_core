#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.specification.country_iso import CountryISO
from scs_core.aqcsv.specification.country_numeric import CountryNumeric

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

print("list ISO...")
for country in CountryISO.instances():
    print(country)
print("-")

print("find ISO...")
iso = "TUN"
iso_country = CountryISO.instance(iso)
print("iso:%s country:%s" % (iso, iso_country))
print(JSONify.dumps(iso_country))
print("-")

print("list Numeric...")
for country in CountryNumeric.instances():
    print(country)
print("-")

print("find Numeric...")
numeric = 788
numeric_country = CountryNumeric.instance(numeric)
print("numeric:%s country:%s" % (numeric, numeric_country))
print(JSONify.dumps(numeric_country))
print("-")


print("equality...")
equality = iso_country == numeric_country
print("iso_country == numeric_country: %s" % equality)
print("-")

