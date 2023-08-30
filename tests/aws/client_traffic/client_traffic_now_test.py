#!/usr/bin/env python3

"""
Created on 14 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.client_traffic.client_traffic import ClientTrafficReport


# --------------------------------------------------------------------------------------------------------------------

now = ClientTrafficReport.now()
print("now: %s" % now)
