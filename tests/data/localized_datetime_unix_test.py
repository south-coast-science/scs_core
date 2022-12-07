#!/usr/bin/env python3

"""
Created on 7 Dec 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------
# run...

datetime = LocalizedDatetime.unix_era_start()
print(datetime)
