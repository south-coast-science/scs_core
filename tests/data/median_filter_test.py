#!/usr/bin/env python3

"""
Created on 14 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.median_filter import MedianFilter


# --------------------------------------------------------------------------------------------------------------------

data = [2, 80, 6, 3, 5]

median_filter = MedianFilter(5)
print(median_filter)
print("-")


for x in data:
    y = median_filter.compute(x)
    print(median_filter)
    print("x: %s y: %s" % (x, y))
    print("-")
