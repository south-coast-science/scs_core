#!/usr/bin/env python3

"""
Created on 24 Aug 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import sys


# --------------------------------------------------------------------------------------------------------------------

print(sys.path)
print("-")

path = os.path.abspath('.')
print(path)

path = os.path.expanduser("~")
print(path)
