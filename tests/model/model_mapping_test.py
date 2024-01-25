#!/usr/bin/env python3

"""
Created on 25 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.model.model_mapping import ModelMapping


# --------------------------------------------------------------------------------------------------------------------
# run...

for name in ModelMapping.names():
    print(name)
    print(ModelMapping.map(name))

