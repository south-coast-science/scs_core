#!/usr/bin/env python3

"""
Created on 15 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_reader import CSVReader


# --------------------------------------------------------------------------------------------------------------------

dialects = CSVReader.list_dialects()

print(dialects)
