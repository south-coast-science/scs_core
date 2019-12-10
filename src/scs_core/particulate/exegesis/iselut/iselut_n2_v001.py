"""
Created on 15 Nov 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

THIS CODE SHALL BE TREATED AS IMMUTABLE. THUS, ANY ALTERATIONS TO EQUATIONS OR STANDARD COEFFICIENTS SHALL BE
PRESENTED AS A NEW CLASS, WITH AN INCREMENTED CLASS VERSION NUMBER.

Coefficients gained from Alphasense OPC-N2 (versus Palas Fidas) data at LHR2 in 2019.

method: Immediate Scaling Error / Look-Up Table (ISELUT), OPC-N2, version 1
Brian Stacey's technique

Scaling	    PM1	        PM2.5	    PM10
0-40	    0.988017	0.9052	    1.039087
40-50	    0.85517	    0.760508	0.845259
50-60	    0.739025	0.651494	0.724954
60-70	    0.61432	    0.538962	0.606225
70-80	    0.4573	    0.40439	    0.456517
80-90	    0.297535	0.255801	0.284946
90-100	    0.186311	0.139511	0.048612
"""

from collections import OrderedDict

from scs_core.particulate.exegesis.iselut.iselut import ISELUT, ISELURow


# --------------------------------------------------------------------------------------------------------------------

class ISELUTN2v1(ISELUT):
    """
    classdocs
    """

    __NAME =                            "iselutn2v1"

    __STANDARD_0_40 = OrderedDict()
    __STANDARD_0_40['pm1'] =            0.988017
    __STANDARD_0_40['pm2p5'] =          0.9052
    __STANDARD_0_40['pm10'] =           1.039087

    __STANDARD_40_50 = OrderedDict()
    __STANDARD_40_50['pm1'] =           0.85517
    __STANDARD_40_50['pm2p5'] =         0.760508
    __STANDARD_40_50['pm10'] =          0.845259

    __STANDARD_50_60 = OrderedDict()
    __STANDARD_50_60['pm1'] =           0.739025
    __STANDARD_50_60['pm2p5'] =         0.651494
    __STANDARD_50_60['pm10'] =          0.724954

    __STANDARD_60_70 = OrderedDict()
    __STANDARD_60_70['pm1'] =           0.61432
    __STANDARD_60_70['pm2p5'] =         0.538962
    __STANDARD_60_70['pm10'] =          0.606225

    __STANDARD_70_80 = OrderedDict()
    __STANDARD_70_80['pm1'] =           0.4573
    __STANDARD_70_80['pm2p5'] =         0.40439
    __STANDARD_70_80['pm10'] =          0.456517

    __STANDARD_80_90 = OrderedDict()
    __STANDARD_80_90['pm1'] =           0.297535
    __STANDARD_80_90['pm2p5'] =         0.255801
    __STANDARD_80_90['pm10'] =          0.284946

    __STANDARD_90_100 = OrderedDict()
    __STANDARD_90_100['pm1'] =          0.186311
    __STANDARD_90_100['pm2p5'] =        0.139511
    __STANDARD_90_100['pm10'] =         0.048612


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return cls.__NAME


    @classmethod
    def standard(cls):
        rows = {
            40: ISELURow(0, 40, cls.__STANDARD_0_40),
            50: ISELURow(40, 50, cls.__STANDARD_40_50),
            60: ISELURow(50, 60, cls.__STANDARD_50_60),
            70: ISELURow(60, 70, cls.__STANDARD_60_70),
            80: ISELURow(70, 80, cls.__STANDARD_70_80),
            90: ISELURow(80, 90, cls.__STANDARD_80_90),
            100: ISELURow(90, 100, cls.__STANDARD_90_100)
        }

        return cls(rows)


    @classmethod
    def uses_external_sht(cls):
        return True
