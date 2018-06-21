"""
Created on 19 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Based-on code
https://github.com/hackscribble/microbit-MPL115A1-barometer/blob/master/microbit-MPL115A1-barometer.py
https://gist.github.com/cubapp/23dd4e91814a995b8ff06f406679abcf
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MPL115A2Datum(JSONable):
    """
    NXP MPL115A2 digital barometer - data interpretation
    """

    # ----------------------------------------------------------------------------------------------------------------

    __PRESSURE_CONV = (115.0 - 50.0) / 1023.0

    __DEFAULT_C25 = 472                                 # T adc counts at 25 ºC
    __COUNTS_PER_DEGREE = -5.35                         # T adc counts per degree centigrade


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __press(cls, p_comp):
        return p_comp * cls.__PRESSURE_CONV + 50.0


    @classmethod
    def __temp(cls, c25, t_adc):
        return (t_adc - c25) / cls.__COUNTS_PER_DEGREE + 25.0


    @classmethod
    def __c25(cls, ref_temp, t_adc):
        return round(t_adc - cls.__COUNTS_PER_DEGREE * (ref_temp - 25.0))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, c25, p_comp, t_adc):
        if p_comp is None or t_adc is None:
            return None

        press = cls.__press(p_comp)
        temp = cls.__temp(c25, t_adc)

        return MPL115A2Datum(t_adc, press, temp)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, t_adc, press, temp):
        """
        Constructor
        """
        self.__t_adc = Datum.int(t_adc)                     # T adc count
        self.__press = Datum.float(press, 1)                # kPa
        self.__temp = Datum.float(temp, 1)                  # ºC


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['prs'] = self.press
        jdict['tmp'] = self.temp

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def c25(self, ref_temp):
        return MPL115A2Datum.__c25(ref_temp, self.__t_adc)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def press(self):
        return self.__press


    @property
    def temp(self):
        return self.__temp


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MPL115A2Datum:{t_adc:%s, press:%s, temp:%s}" % (self.__t_adc, self.press, self.temp)
