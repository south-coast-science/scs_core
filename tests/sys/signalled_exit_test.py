#!/usr/bin/env python3

"""
Created on 26 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.sys.signalled_exit import SignalledExit


# --------------------------------------------------------------------------------------------------------------------
# run...


listener = SignalledExit.construct("test", True)
print(listener)

while True:
    time.sleep(1)

