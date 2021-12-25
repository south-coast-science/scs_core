#!/usr/bin/env python3

"""
Created on 15 Dec 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sys.node import Node


# --------------------------------------------------------------------------------------------------------------------
# run...

result = Node.ping('8.8.8.8', ttl=128)
print("ping result: %s" % result)

result = Node.is_connected('aws.amazon.com')
print("is_connected result: %s" % result)

