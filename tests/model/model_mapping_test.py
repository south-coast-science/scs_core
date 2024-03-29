#!/usr/bin/env python3

"""
Created on 25 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.model.model_map import ModelMap


# --------------------------------------------------------------------------------------------------------------------
# run...

for name in ModelMap.names():
    print(name)
    print(ModelMap.map(name))

