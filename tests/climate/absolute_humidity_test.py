#!/usr/bin/env python3

"""
Created on 12 Feb 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.aqua-calc.com/calculate/humidity
"""

from scs_core.climate.absolute_humidity import AbsoluteHumidity


# --------------------------------------------------------------------------------------------------------------------

for t in range(-10, 41, 10):
    for rh in range(0, 99, 10):
        ah = AbsoluteHumidity.from_rh_t(rh, t)

        print("t:%3d rh:%3d -> ah:%5.1f" % (t, rh, round(ah, 3)))

    print("-")
