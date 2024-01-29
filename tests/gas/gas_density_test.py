#!/usr/bin/env python3

"""
Created on 13 Feb 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.apis.ac.uk/unit-conversion
"""

from scs_core.gas.gas import Gas


# --------------------------------------------------------------------------------------------------------------------

gases = ('CO', 'CO2', 'NO', 'NO2', 'O3', 'SO2')

for gas in gases:
    print("gas: %s conc: 1 ppb..." % gas)

    # variable T, P...
    for t in range(-10, 41, 10):
        for p in [99.3, 100.3, 101.3, 102.3]:
            dens = Gas.density(gas, 1, t, p)
            conc = Gas.concentration(gas, dens, t, p)

            print("t:%3d p:%5.1f -> dens:%6.3f -> conc(calc):%6.3f" % (t, p, round(dens, 3), round(conc, 3)))

        print('-')

    # STP...
    dens = Gas.density_stp(gas, 1)
    conc = Gas.concentration_stp(gas, dens)

    print("STP -> dens:%6.3f -> conc(calc):%6.3f" % (round(dens, 3), round(conc, 3)))

    print('=')


