#!/usr/bin/env python3

"""
Created on 21 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

datetime_str = 'Sat, 11 Sep 2021 08:47:47 GMT'
print(datetime_str)

datetime = LocalizedDatetime.construct_from_s3(datetime_str)
print(datetime)

