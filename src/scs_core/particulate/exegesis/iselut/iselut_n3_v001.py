"""
Created on 15 Nov 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

THIS CODE SHALL BE TREATED AS IMMUTABLE. THUS, ANY ALTERATIONS TO EQUATIONS OR STANDARD COEFFICIENTS SHALL BE
PRESENTED AS A NEW CLASS, WITH AN INCREMENTED CLASS VERSION NUMBER.

Coefficients gained from Alphasense OPC-N3 (versus Palas Fidas) data at Gatwick, Nov 1 - 14 2019.

method: Immediate Scaling Error / Look-Up Table (ISELUT), OPC-N3, version 1
Brian Stacey's technique

Note: divide by error for correction

hmd.min hmd.avg hmd.max     pm1.avg     pm1.stdev   pm2p5.avg   pm2p5.stdev     pm10.avg    pm10.stdev
22.5	26.6	29.9	    0.268	    0.169	    0.41	    0.381	        0.089	    0.038
30.0	36.1	39.9	    0.676	    0.268	    1.691	    0.912	        0.238	    0.069
40.0	46.3	49.9	    0.911	    0.483	    2.48	    3.415	        0.46	    0.392
50.0	51.0	53.5	    1.244	    0.644	    3.179	    4.07	        0.715	    0.538
61.2	61.2	61.2	    0.568       0.647		0.239
"""

from collections import OrderedDict

from scs_core.particulate.exegesis.iselut.iselut import ISELUT, ISELURow


# --------------------------------------------------------------------------------------------------------------------

class ISELUTN3v1(ISELUT):
    """
    classdocs
    """

    __NAME =                            "iselutn3v1"

    __STANDARD_0_30 = OrderedDict()
    __STANDARD_0_30['pm1'] =            0.268
    __STANDARD_0_30['pm2p5'] =          0.41
    __STANDARD_0_30['pm10'] =           0.089

    __STANDARD_30_40 = OrderedDict()
    __STANDARD_30_40['pm1'] =           0.676
    __STANDARD_30_40['pm2p5'] =         1.691
    __STANDARD_30_40['pm10'] =          0.238

    __STANDARD_40_50 = OrderedDict()
    __STANDARD_40_50['pm1'] =           0.911
    __STANDARD_40_50['pm2p5'] =         2.48
    __STANDARD_40_50['pm10'] =          0.46

    __STANDARD_50_100 = OrderedDict()
    __STANDARD_50_100['pm1'] =           1.244
    __STANDARD_50_100['pm2p5'] =         3.179
    __STANDARD_50_100['pm10'] =          0.715


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return cls.__NAME


    @classmethod
    def standard(cls):
        rows = {
            30: ISELURow(0, 30, cls.__STANDARD_0_30),
            40: ISELURow(30, 40, cls.__STANDARD_30_40),
            50: ISELURow(40, 50, cls.__STANDARD_40_50),
            100: ISELURow(50, 100, cls.__STANDARD_50_100)
        }

        return cls(rows)


    # ----------------------------------------------------------------------------------------------------------------

    def _interpret(self, species, pm, rh):
        if pm is None or rh is None:
            return None

        print("ISELUTN3v1")

        row = self._row(rh)

        return pm / row.error(species, rh)
