#!/usr/bin/env python3

"""
Created on 28 Nov 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify
from scs_core.estate.software_version import SoftwareVersion


# --------------------------------------------------------------------------------------------------------------------

x = SoftwareVersion.construct_from_jdict("1.23")
print("x: %s" % x)

a = SoftwareVersion.construct_from_jdict("1.23.45-text")
print("a: %s" % a)

b = SoftwareVersion.construct_from_jdict("1.123.45")
print("b: %s" % b)

print("a == b: %s" % str(a == b))
print("a < b: %s" % str(a < b))

c = None
print("a == None: %s" % str(a == c))

c = "hello"
print("a == str: %s" % str(a == c))

c = 1
print("a == int: %s" % str(a == c))

print(JSONify.dumps(a, sortable=True))
