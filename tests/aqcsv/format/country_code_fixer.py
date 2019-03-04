#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.aqua-calc.com/calculate/humidity
"""

import sys


# --------------------------------------------------------------------------------------------------------------------

numeric = ''
name = ''
iso = ''

coll = 0

for line in sys.stdin:
    cell = line.strip()

    if coll == 0:
        numeric = cell
        coll = 1

    elif coll == 1:
        name = cell
        coll = 2

    else:
        iso = cell

        print('"%s","%s","%s"' % (numeric, name, iso))
        sys.stdout.flush()

        coll = 0
