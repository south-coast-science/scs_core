#!/usr/bin/env python3

"""
Created on 22 May 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.checkpoint_generator import CheckpointGenerator
from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

generator = CheckpointGenerator.construct("**:/15:00")
print(generator)
print("-")

hours = 23
seconds = 0.1

for minutes in range(0, 60):
    next_checkpoint = generator.next(hours, minutes, seconds)
    print("hours: %02d minutes: %02d seconds: %04.1f - %s" % (hours, minutes, seconds, next_checkpoint))

print("=")

generator = CheckpointGenerator.construct("**:**:/30")
print(generator)
print("-")

now = LocalizedDatetime.now()
print("now: %s" % now)
print("-")

checkpoint = generator.next_localised_datetime(now)

for _ in range(10):
    print("checkpoint: %s" % checkpoint)
    checkpoint = generator.next_localised_datetime(checkpoint)
