#!/usr/bin/env python3

"""
Created on 21 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import Date


# --------------------------------------------------------------------------------------------------------------------

date_str = '2-23-07-21'
print("%s: is valid: %s" % (date_str, Date.is_valid_iso_format(date_str)))
print("-")

date_str = '2023-7-21'
print("%s: is valid: %s" % (date_str, Date.is_valid_iso_format(date_str)))
print("-")

date_str = '21-07-2023'
print("%s: is valid: %s" % (date_str, Date.is_valid_iso_format(date_str)))
print("-")

date_str = '2023-07-21'
print("%s: is valid: %s" % (date_str, Date.is_valid_iso_format(date_str)))
print("-")

date_str = None
print("%s: is valid: %s" % (date_str, Date.is_valid_iso_format(date_str)))
print("-")
