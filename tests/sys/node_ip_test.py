#!/usr/bin/env python3

"""
Created on 2 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.sys.node import Node


# --------------------------------------------------------------------------------------------------------------------
# run...

ip = Node.ipv4_address()
print("ipv4 address: %s" % str(ip))

start_time = time.time()

for dot_decimal in Node.scan(0, 255):
    print("ping %s" % dot_decimal)
    sys.stdout.flush()

elapsed_time = time.time() - start_time

print("elapsed: %0.3f" % elapsed_time)
