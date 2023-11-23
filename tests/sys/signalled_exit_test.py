#!/usr/bin/env python3

"""
Created on 26 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.sys.logging import Logging
from scs_core.sys.signalled_exit import SignalledExit


# --------------------------------------------------------------------------------------------------------------------
# run...

Logging.config('signalled_exit_test.py', verbose=True)
logger = Logging.getLogger()

listener = SignalledExit.construct()
print(listener)

while True:
    time.sleep(1)

