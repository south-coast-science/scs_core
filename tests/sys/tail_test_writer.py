#!/usr/bin/env python3

"""
Created on 20 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import sys
import time


# --------------------------------------------------------------------------------------------------------------------

path = os.path.expanduser('~/SCS/scs_core/tests/sys/tail_test.json')

file = open(path, 'w')

try:
    for i in range(11):
        file.write("line: %2d\n" % i)
        file.flush()

        print("line: %2d" % i)
        sys.stdout.flush()

        time.sleep(1)

finally:
    file.close()

while True:
    time.sleep(1)
