"""
Created on 19 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Pt1000Datum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __temp(v20, v):
        temp = (v - v20) * 1000.0 + 20.0            # V = V20C + 0.001 * (T - T20C), sensitivity is 1.0 mV / K

        return round(temp, 1)


    @staticmethod
    def __v20(ref_temp, v):
        v20 = v - (ref_temp - 20.0) / 1000.0        # V = V20C + 0.001 * (T - T20C), sensitivity is 1.0 mV / K

        return round(v20, 6)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, calib, v):
        if v is None:
            return None

        temp = cls.__temp(calib.v20, v)

        return Pt1000Datum(v, temp)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, v, temp=None):
        """
        Constructor
        """
        self.__v = Datum.float(v, 6)                # Volts
        self.__temp = Datum.float(temp, 1)          # temperature °C


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['v'] = self.v
        jdict['tmp'] = self.temp

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def v20(self, ref_temp):
        return Pt1000Datum.__v20(ref_temp, self.__v)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def v(self):
        return self.__v


    @property
    def temp(self):
        return self.__temp


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Pt1000Datum:{v:%s, temp:%s}" % (self.v, self.temp)
