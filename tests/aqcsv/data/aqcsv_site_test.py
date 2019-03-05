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

site = AQCSVSite.construct_from_code(code)
print("site: %s" % site)
print("country: %s" % site.country())
print("code: %s" % site.as_code())
print("json: %s" % JSONify.dumps(site.as_json()))
print("-")

code = "124MM456789123"
print("code: %s" % code)

site = AQCSVSite.construct_from_code(code)
print("site: %s" % site)
print("country: %s" % site.country())
print("code: %s" % site.as_code())
print("json: %s" % JSONify.dumps(site.as_json()))
print("-")

code = "999MM456789123"
print("code: %s" % code)

site = AQCSVSite.construct_from_code(code)
print("site: %s" % site)
print("country: %s" % site.country())
print("code: %s" % site.as_code())
print("json: %s" % JSONify.dumps(site.as_json()))
print("-")
