#!/usr/bin/env python3

"""
Created on 2 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------
# run...

ip = Host.ipv4_address()
print("ipv4 address: %s" % str(ip))

start_time = time.time()

for dot_decimal in Host.scan_accessible_subnets():
    print("found: %s" % dot_decimal)
    sys.stdout.flush()

elapsed_time = time.time() - start_time

print("elapsed: %0.3f" % elapsed_time)
