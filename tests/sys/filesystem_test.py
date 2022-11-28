#!/usr/bin/env python3

"""
Created on 10 Sep 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

path = os.path.expanduser('~/SCS/conf')

files = Filesystem.ls(path)
for file in files:
    print(file)
