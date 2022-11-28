#!/usr/bin/env python3

"""
Created on 25 Nov 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

DATA_STORE = "/srv/removable_data_storage"
# DATA_STORE = "/"

try:
    on_root = Filesystem.is_on_root_filesystem(DATA_STORE)
    print("on_root: %s" % on_root)

except FileNotFoundError:
    print("on_root: file not found")

try:
    used = Filesystem.percentage_used(DATA_STORE)
    print("used: %s%%" % used)

except FileNotFoundError:
    print("used: file not found")
