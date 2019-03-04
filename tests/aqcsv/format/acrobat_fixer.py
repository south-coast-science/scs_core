#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Converts Acrobat cell-per-line to CSV format
"""

import sys


# --------------------------------------------------------------------------------------------------------------------

colls = 4



coll = 0
cells = []

for line in sys.stdin:
    cell = line.strip()

    cells.append(cell)
    coll += 1

    if coll < colls:
        continue

    row = '' + ','.join(['"' + cell + '"' for cell in cells])

    print(row)
    sys.stdout.flush()

    coll = 0
    cells = []
