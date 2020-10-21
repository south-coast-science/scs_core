#!/usr/bin/env python3

"""
Created on 22 May 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.checkpoint_generator import CheckpointGenerator
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.timedelta import Timedelta

# --------------------------------------------------------------------------------------------------------------------

generator = CheckpointGenerator.construct("**:/15:00")
print(generator)
print("-")

hours = 1
seconds = 0

for minutes in range(59, -1, -1):
    prev_checkpoint = generator.prev(hours, minutes, seconds)
    print("hours: %02d minutes: %02d seconds: %04.1f - %s" % (hours, minutes, seconds, prev_checkpoint))

print("=")

checkpoint = CheckpointGenerator.construct("23:59:59")
print(checkpoint)
print("-")

ldt = LocalizedDatetime.construct_from_iso8601("2020-05-22T23:59:59Z")
print("ldt: %s" % ldt)

prev_checkpoint = checkpoint.prev_localised_datetime(ldt)
print("prev_checkpoint: %s" % prev_checkpoint)

print("-")

now = LocalizedDatetime.now()
print("now: %s" % now)

prev_checkpoint = checkpoint.prev_localised_datetime(now)
print("prev_checkpoint: %s" % prev_checkpoint)

print("=")

generator = CheckpointGenerator.construct("**:**:/30")
print(generator)
print("-")

now = LocalizedDatetime.now()
print("now: %s" % now)
print("-")

checkpoint = generator.prev_localised_datetime(now)

for _ in range(10):
    checkpoint = generator.prev_localised_datetime(checkpoint)
    print("checkpoint: %s" % checkpoint)

    checkpoint = LocalizedDatetime(checkpoint - Timedelta(seconds=1))   # nudge back in time
