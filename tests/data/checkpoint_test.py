#!/usr/bin/env python3

"""
Created on 24 Oct 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.checkpoint_generator import CheckpointGenerator
from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

generator = CheckpointGenerator.construct("**:/01:00")
print(generator)
print("-")

while True:
    now = LocalizedDatetime.now().utc()
    print("now: %s" % now)

    next_checkpoint = generator.next_localised_datetime(now)
    print("next: %s" % str(next_checkpoint))
    print("-")

    time.sleep(1)
