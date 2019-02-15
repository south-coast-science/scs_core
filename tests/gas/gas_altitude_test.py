#!/usr/bin/env python3

"""
Created on 14 Feb 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://keisan.casio.com/exec/system/1224579725
"""

from scs_core.gas.gas import Gas


# --------------------------------------------------------------------------------------------------------------------

p_0 = Gas.STP_PRESSURE

for t in range(-10, 41, 10):
    for alt in range(0, 4001, 1000):
        p_alt = Gas.p_alt(p_0, t, alt)
        calc_p_0 = Gas.p_0(p_alt, t, alt)

        print("t:%3d alt:%7.1f -> p_alt:%6.1f -> p_0(calc):%6.3f" % (t, alt, round(p_alt, 3), round(calc_p_0, 3)))

    print('-')

p_alt = Gas.p_alt(Gas.STP_PRESSURE, 8.6, 26)
print("t:%3d alt:%7.1f -> p_alt:%6.1f" % (8.6, 26, round(p_alt, 3)))
