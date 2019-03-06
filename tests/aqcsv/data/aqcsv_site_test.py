#!/usr/bin/env python3

"""
Created on 5 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.data.aqcsv_site import AQCSVSite
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

code = "120456789123"
print("code: %s" % code)

site1 = AQCSVSite.construct_from_code(code)
print("site1: %s" % site1)
print("country: %s" % site1.country())
print("code: %s" % site1.as_code())
print("json: %s" % JSONify.dumps(site1.as_json()))
print("-")

code = "124MM456789123"
print("code: %s" % code)

site2 = AQCSVSite.construct_from_code(code)
print("site2: %s" % site2)
print("country: %s" % site2.country())
print("code: %s" % site2.as_code())
print("json: %s" % JSONify.dumps(site2.as_json()))
print("-")

code = "999MM456789123"
print("code: %s" % code)

site3 = AQCSVSite.construct_from_code(code)
print("site3: %s" % site3)
print("country: %s" % site3.country())
print("code: %s" % site3.as_code())
print("json: %s" % JSONify.dumps(site3.as_json()))
print("-")

print("equality...")
equality = site2 == site3
print("site2 == site3: %s" % equality)
print("-")

code = site3.as_code()
remade = AQCSVSite.construct_from_code(code)
equality = remade == site3
print("remade == site3: %s" % equality)
print("-")
