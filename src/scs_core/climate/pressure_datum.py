"""
Created on 8 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PressureDatum(JSONable):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        actual_press = jdict.get('pA')
        sl_press = jdict.get('p0')
        temp = jdict.get('tmp')

        return cls(actual_press, sl_press, temp)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def _sl_press(cls, actual_press, temp, altitude):
        if temp is None or altitude is None:
            return None

        return (actual_press * 9.80665 * altitude) / (287 * (273 + temp + (altitude / 400))) + actual_press


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, actual_press, sl_press, temp):
        """
        Constructor
        """
        self.__actual_press = Datum.float(actual_press, 3)          # kPa
        self.__sl_press = Datum.float(sl_press, 3)                  # kPa

        self.__temp = Datum.float(temp, 1)                          # °C


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['pA'] = self.actual_press

        if self.sl_press is not None:
            jdict['p0'] = self.sl_press

        if self.temp is not None:
            jdict['tmp'] = self.temp

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def actual_press(self):
        return self.__actual_press


    @property
    def sl_press(self):
        return self.__sl_press


    @property
    def temp(self):
        return self.__temp
