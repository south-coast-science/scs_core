#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Converts Acrobat cell-per-line data to CSV format
"""

import sys


# --------------------------------------------------------------------------------------------------------------------

columns = 2


# --------------------------------------------------------------------------------------------------------------------

cells = []
col = 0

try:
    for line in sys.stdin:
        cell = line.strip()

        cells.append(cell)
        col += 1

        if col < columns:
            continue

        row = '' + ','.join(['"' + cell + '"' for cell in cells])

        print(row)
        sys.stdout.flush()

        cells = []
        col = 0

except KeyboardInterrupt:
    pass
