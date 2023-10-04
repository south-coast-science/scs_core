#!/usr/bin/env python3

"""
Created on 8 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.client_traffic.client_traffic_intercourse import ClientTrafficRequest


# --------------------------------------------------------------------------------------------------------------------

period = '2023'
is_valid = ClientTrafficRequest.is_valid_period(period)
print("%s: is_valid: %s" % (period, is_valid))

period = '2023-01'
is_valid = ClientTrafficRequest.is_valid_period(period)
print("%s: is_valid: %s" % (period, is_valid))

period = '2023-01-16'
is_valid = ClientTrafficRequest.is_valid_period(period)
print("%s: is_valid: %s" % (period, is_valid))

period = None
is_valid = ClientTrafficRequest.is_valid_period(period)
print("%s: is_valid: %s" % (period, is_valid))

period = 1
is_valid = ClientTrafficRequest.is_valid_period(period)
print("%s: is_valid: %s" % (period, is_valid))

period = '2023-01-163'
is_valid = ClientTrafficRequest.is_valid_period(period)
print("%s: is_valid: %s" % (period, is_valid))

period = '2023-01-40'
is_valid = ClientTrafficRequest.is_valid_period(period)
print("%s: is_valid: %s" % (period, is_valid))

period = '2023-20-13'
is_valid = ClientTrafficRequest.is_valid_period(period)
print("%s: is_valid: %s" % (period, is_valid))
print("-")


