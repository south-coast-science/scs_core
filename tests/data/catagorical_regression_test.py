#!/usr/bin/env python3

"""
Created on 11 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.categorical_regression import CategoricalRegression


# --------------------------------------------------------------------------------------------------------------------

reg = CategoricalRegression()

reg.append(None, "hello")
print(reg)

reg.append(None, "hello")
print(reg)
print("-")

_, midpoint = reg.midpoint()

print("min: %s" % reg.min())
print("midpoint: %s" % midpoint)
print("max: %s" % reg.max())
print("-")

reg.append(None, "goodbye")
print(reg)

_, midpoint = reg.midpoint()

print("min: %s" % reg.min())
print("midpoint: %s" % midpoint)
print("max: %s" % reg.max())
print("-")
