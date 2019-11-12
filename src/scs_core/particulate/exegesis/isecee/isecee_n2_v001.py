"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

THIS CODE SHALL BE TREATED AS IMMUTABLE. THUS, ANY ALTERATIONS TO EQUATIONS OR STANDARD COEFFICIENTS SHALL BE
PRESENTED AS A NEW CLASS, WITH AN INCREMENTED CLASS VERSION NUMBER.

Coefficients gained from Alphasense OPC-N2 (versus Palas Fidas) data at LHR2, from Feb - Apr 2019.

method: Immediate Scaling Error / Curve is Elbow Exponential (ISECEE), OPC-N2, version 1

domain: 0 <= rH <= max_rh
model: error = ceLOW * e ^ (cxLOW * rH) where rH < elbow
model: error = ceHIGH * e ^ (cxHIGH * rH) where rH => elbow
range: PM / error
"""

from collections import OrderedDict

from scs_core.particulate.exegesis.isecee.isecee import ISECEE


# --------------------------------------------------------------------------------------------------------------------

class ISECEEN2v1(ISECEE):
    """
    classdocs
    """

    __NAME =                            "iseceen2v1"

    __STANDARD_CE_LOW = OrderedDict()
    __STANDARD_CE_LOW['pm1'] =          0.6029
    __STANDARD_CE_LOW['pm2p5'] =        0.6208
    __STANDARD_CE_LOW['pm10'] =         0.5375

    __STANDARD_CX_LOW = OrderedDict()
    __STANDARD_CX_LOW['pm1'] =          0.0195
    __STANDARD_CX_LOW['pm2p5'] =        0.0208
    __STANDARD_CX_LOW['pm10'] =         0.0213

    __STANDARD_CE_HIGH = OrderedDict()
    __STANDARD_CE_HIGH['pm1'] =         0.1605
    __STANDARD_CE_HIGH['pm2p5'] =       0.1924
    __STANDARD_CE_HIGH['pm10'] =        0.0177

    __STANDARD_CX_HIGH = OrderedDict()
    __STANDARD_CX_HIGH['pm1'] =         0.0398
    __STANDARD_CX_HIGH['pm2p5'] =       0.0389
    __STANDARD_CX_HIGH['pm10'] =        0.0728

    __STANDARD_CE = OrderedDict()
    __STANDARD_CE['low'] = __STANDARD_CE_LOW
    __STANDARD_CE['high'] = __STANDARD_CE_HIGH

    __STANDARD_CX = OrderedDict()
    __STANDARD_CX['low'] = __STANDARD_CX_LOW
    __STANDARD_CX['high'] = __STANDARD_CX_HIGH

    __STANDARD_rH_ELBOW =               61                      # percent relative humidity

    __STANDARD_MAX_rH_PM1 =             100
    __STANDARD_MAX_rH_PM2p5 =           100
    __STANDARD_MAX_rH_PM10 =            85


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return cls.__NAME


    @classmethod
    def standard(cls):
        return cls(cls.__STANDARD_CE, cls.__STANDARD_CX, cls.__STANDARD_rH_ELBOW,
                   cls.__STANDARD_MAX_rH_PM1, cls.__STANDARD_MAX_rH_PM2p5, cls.__STANDARD_MAX_rH_PM10)
