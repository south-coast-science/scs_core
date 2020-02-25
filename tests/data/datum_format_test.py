#!/usr/bin/env python3

"""
Created on 10 Dec 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datum import Format


# --------------------------------------------------------------------------------------------------------------------

value = {"a": 1, "b": 2}
print(Format.collection(value))
print("-")

value = [1, 2, 3]
print(Format.collection(value))
print("-")

value = (1, 2, 3)
print(Format.collection(value))
print("-")

value = [1, {"a": 1, "b": [1, {"a": 1, "b": 2}, 3]}, 3]
print(Format.collection(value))
