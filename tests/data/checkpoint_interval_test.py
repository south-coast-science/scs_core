#!/usr/bin/env python3

"""
Created on 11 Feb 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.checkpoint_generator import CheckpointGenerator


# --------------------------------------------------------------------------------------------------------------------

specification = "**:**:/10"
print(specification)
generator = CheckpointGenerator.construct(specification)
print(generator)
print("min_interval: %s" % generator.min_interval())
print("-")

specification = "**:/5:00"
print(specification)
generator = CheckpointGenerator.construct(specification)
print(generator)
print("min_interval: %s" % generator.min_interval())
print("-")

specification = "**:00:00"
print(specification)
generator = CheckpointGenerator.construct(specification)
print(generator)
print("min_interval: %s" % generator.min_interval())
print("-")

specification = "00:00:00"
print(specification)
generator = CheckpointGenerator.construct(specification)
print(generator)
print("min_interval: %s" % generator.min_interval())
print("-")

specification = "00:/1:00"
print(specification)
generator = CheckpointGenerator.construct(specification)
print(generator)
print("min_interval: %s" % generator.min_interval())
print("-")
