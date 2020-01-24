#!/usr/bin/env python3

"""
Created on 20 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from scs_core.sys.tail import Tail


# --------------------------------------------------------------------------------------------------------------------

path = os.path.expanduser('~/SCS/scs_core/tests/sys/tail_test.json')

tail = Tail.construct(path)
print(tail)

try:
    tail.open()

    for message in tail.readlines():
        print("got: %s" % message)

finally:
    tail.close()
