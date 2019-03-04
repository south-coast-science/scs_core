#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.specification.agency import Agency
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

Agency.load()

print("list...")
for agency in Agency.instances():
    print(agency)
print("-")

print("find...")
code = "LBL"
agency = Agency.find(code)
print("code:%s agency:%s" % (code, agency))
print(JSONify.dumps(agency))
print("-")

code = "XXX"
agency = Agency.find(code)
print("code:%s agency:%s" % (code, agency))
print("-")
