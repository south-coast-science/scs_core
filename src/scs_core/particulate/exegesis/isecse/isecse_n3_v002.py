"""
Created on 15 Nov 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

THIS CODE SHALL BE TREATED AS IMMUTABLE. THUS, ANY ALTERATIONS TO EQUATIONS OR STANDARD COEFFICIENTS SHALL BE
PRESENTED AS A NEW CLASS, WITH AN INCREMENTED CLASS VERSION NUMBER.

Coefficients gained from Alphasense OPC-N3 (versus Palas Fidas) data at Gatwick, Nov 1 - 14 2019.
Uses Praxis external SHT31.

method: Immediate Scaling Error / Curve is Single Exponential (ISECSE), OPC-N3, version 1

domain: 0 <= rH <= max_rh
model: error = ce * e ^ (cx * rH)
range: PM / error
"""

from collections import OrderedDict

from scs_core.particulate.exegesis.isecse.isecse import ISECSE


# --------------------------------------------------------------------------------------------------------------------

class ISECSEN3v2(ISECSE):
    """
    classdocs
    """

    __NAME =                            "isecsen3v2"

    __STANDARD_CE = OrderedDict()
    __STANDARD_CE['pm1'] =              0.089
    __STANDARD_CE['pm2p5'] =            0.0851
    __STANDARD_CE['pm10'] =             0.0452

    __STANDARD_CX = OrderedDict()
    __STANDARD_CX['pm1'] =              0.0321
    __STANDARD_CX['pm2p5'] =            0.0461
    __STANDARD_CX['pm10'] =             0.0687

    __STANDARD_MAX_rH_PM1 =             100
    __STANDARD_MAX_rH_PM2p5 =           100
    __STANDARD_MAX_rH_PM10 =            85


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return cls.__NAME


    @classmethod
    def standard(cls):
        return cls(cls.__STANDARD_CE, cls.__STANDARD_CX,
                   cls.__STANDARD_MAX_rH_PM1, cls.__STANDARD_MAX_rH_PM2p5, cls.__STANDARD_MAX_rH_PM10)
