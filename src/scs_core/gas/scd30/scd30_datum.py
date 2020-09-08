"""
Created on 7 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"co2": 1265.0, "tmp": 28.9, "hmd": 51.0}
"""

from collections import OrderedDict
from numbers import Number

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SCD30Datum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        co2 = jdict.get('co2')
        temp = jdict.get('tmp')
        humid = jdict.get('hmd')

        return SCD30Datum(co2, temp, humid)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, co2, temp, humid):
        """
        Constructor
        """
        self.__co2 = Datum.float(co2, 1)                        # concentration         ppm
        self.__temp = Datum.float(temp, 1)                      # temperature           °C
        self.__humid = Datum.float(humid, 1)                    # relative humidity     %


    # ----------------------------------------------------------------------------------------------------------------
    # Support for averaging...

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(other)

        co2 = self.co2 + other.co2
        temp = self.temp + other.temp
        humid = self.humid + other.humid

        return SCD30Datum(co2, temp, humid)


    def __truediv__(self, other):
        if not isinstance(other, Number):
            raise TypeError(other)

        co2 = self.co2 / other
        temp = self.temp / other
        humid = self.humid / other

        return SCD30Datum(co2, temp, humid)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['co2'] = self.co2
        jdict['tmp'] = self.temp
        jdict['hmd'] = self.humid

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def co2(self):
        return self.__co2


    @property
    def temp(self):
        return self.__temp


    @property
    def humid(self):
        return self.__humid


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SCD30Datum:{co2:%s, temp:%s, humid:%s}" % (self.co2, self.temp, self.humid)
