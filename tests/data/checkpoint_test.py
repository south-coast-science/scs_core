#!/usr/bin/env python3

"""
Created on 24 Oct 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.checkpoint import Checkpoint
from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

checkpoint = Checkpoint.construct("**:/15:00")

print(checkpoint)
print("-")

hours = 23
seconds = 0.1

for minutes in range(0, 60):
        next_checkpoint = checkpoint.next(hours, minutes, seconds)
        print("hours: %02d minutes: %02d seconds: %04.1f - %s" % (hours, minutes, seconds, next_checkpoint))


while True:
    now = LocalizedDatetime.now()
    print(now)

    next_checkpoint = checkpoint.next_localised_datetime(now)
    print("%s" % str(next_checkpoint))
    print("-")

    time.sleep(1)
