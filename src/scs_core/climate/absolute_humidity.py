"""
Created on 12 Feb 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.aqua-calc.com/calculate/humidity
"""

from math import exp


# --------------------------------------------------------------------------------------------------------------------

class AbsoluteHumidity(object):
    """
    classdocs
    """

    __TCK =     647.096                     # critical temperature (K)
    __PC = 22064000.0                       # critical pressure (Pa)

    __RW =      461.52                      # specific gas constant for water vapour

    __A1 =       -7.85951783
    __A2 =        1.84408259
    __A3 =      -11.7866497
    __A4 =       22.6807411
    __A5 =      -15.9618719
    __A6 =        1.80122502


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def from_rh_t(cls, rh, t):              # %, °C -> g/m3
        tk = t + 273.15

        theta = 1.0 - (tk / cls.__TCK)

        sequence = (cls.__A1 * theta) + (cls.__A2 * pow(theta, 1.5)) + (cls.__A3 * pow(theta, 3.0)) + \
                   (cls.__A4 * pow(theta, 3.5)) + (cls.__A5 * pow(theta, 4.0)) + (cls.__A6 * pow(theta, 7.5))

        ln_pws_pc = (cls.__TCK / tk) * sequence

        pws = exp(ln_pws_pc) * cls.__PC

        pw = pws * (rh / 100.0)

        ah = pw / (cls.__RW * tk)

        return ah * 1000.0
