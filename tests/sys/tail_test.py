#!/usr/bin/env python3

"""
Created on 20 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sys.tail import Tail


# --------------------------------------------------------------------------------------------------------------------

path = '/home/pi/SCS/scs_core/tests/csv/event_test.csv'

tail = Tail.construct(path)
print(tail)

try:
    tail.open()

    for message in tail.readlines():
        print("got: %s" % message)

finally:
    tail.close()
