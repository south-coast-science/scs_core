#!/usr/bin/env python3

"""
Created on 19 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.min_list import MinList


# --------------------------------------------------------------------------------------------------------------------

min_list = MinList(4)
print(min_list)
print("-")

mins = (5, 60, 60, 60, 7321, 58, 61, 48, 4, 7322)

for candidate in mins:
    print("candidate: %s" % candidate)
    min_list.append(candidate)
    print(min_list)
    print("max_minimum: %s" % min_list.max())
    print("-")

