#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.specification.agency import Agency
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

print("list...")
for agency in Agency.instances():
    print(agency)
print("-")

print("find...")
code = "XXX"
agency = Agency.instance(code)
print("code:%s agency:%s" % (code, agency))
print("-")

code = "LBL"
agency = Agency.instance(code)
print("code:%s agency:%s" % (code, agency))

jstr = JSONify.dumps(agency)
print(jstr)
print("-")

print("equality...")
jdict = agency.as_json()
remade = Agency.construct_from_jdict(jdict)
print(remade)

equality = remade == agency
print("remade == agency: %s" % equality)
print("-")
