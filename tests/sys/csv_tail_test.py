#!/usr/bin/env python3

"""
Created on 26 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from scs_core.csv.csv_reader import CSVReader
from scs_core.sys.tail import Tail


# --------------------------------------------------------------------------------------------------------------------

path = os.path.expanduser('~/SCS/scs_core/tests/sys/tail_test.json')

tail = Tail.construct(path)
tail.open()
print(tail)

reader = CSVReader(tail)
print(reader)
print("-")

try:
    for message in reader.rows():
        print("got: %s" % message)

finally:
    reader.close()
    tail.close()

    print("done")
