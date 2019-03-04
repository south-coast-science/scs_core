#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Converts Acrobat cell-per-line to CSV format
"""

import sys


# --------------------------------------------------------------------------------------------------------------------

c1 = ''
c2 = ''
c3 = ''

coll = 0

for line in sys.stdin:
    cell = line.strip()

    if coll == 0:
        c1 = cell
        coll = 1

    # elif coll == 1:
    #     name = cell
    #     coll = 2

    else:
        c2 = cell

        print('"%s","%s"' % (c1, c2))
        # print('"%s","%s","%s"' % (numeric, name, iso))
        sys.stdout.flush()

        coll = 0
