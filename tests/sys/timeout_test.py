#!/usr/bin/env python3

"""
Created on 17 Sep 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.sys.timeout import Timeout


# --------------------------------------------------------------------------------------------------------------------
# run...

timeout = Timeout(5)
print(timeout)
print("-")

try:
    with timeout:
        time.sleep(10)
        print("slept")

except TimeoutError:
    print("TimeoutError")

finally:
    print("done")
