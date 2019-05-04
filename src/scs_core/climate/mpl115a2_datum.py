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

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class MPL115A2Datum(JSONable):
    """
    NXP MPL115A2 digital barometer - data interpretation
    """

    # ----------------------------------------------------------------------------------------------------------------

    __PRESSURE_CONV = (115.0 - 50.0) / 1023.0

    __DEFAULT_C25 = 472                                 # T adc counts at 25 °C
    __COUNTS_PER_DEGREE = -5.35                         # T adc counts per degree centigrade


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __actual_press(cls, p_comp):
        return p_comp * cls.__PRESSURE_CONV + 50.0


    @classmethod
    def __sl_press(cls, actual_press, temp, altitude):
        if temp is None or altitude is None:
            return None

        return (actual_press * 9.80665 * altitude) / (287 * (273 + temp + (altitude / 400))) + actual_press


    @classmethod
    def __temp(cls, c25, t_adc):
        if c25 is None:
            return None

        return (t_adc - c25) / cls.__COUNTS_PER_DEGREE + 25.0


    @classmethod
    def __c25(cls, ref_temp, t_adc):
        return round(t_adc - cls.__COUNTS_PER_DEGREE * (ref_temp - 25.0))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, c25, p_comp, t_adc, altitude):
        if p_comp is None or t_adc is None:
            return None

        temp = cls.__temp(c25, t_adc)

        actual_press = cls.__actual_press(p_comp)
        sl_press = cls.__sl_press(actual_press, temp, altitude)

        return MPL115A2Datum(actual_press, sl_press, t_adc, temp)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, actual_press, sl_press, t_adc, temp):
        """
        Constructor
        """
        self.__actual_press = Datum.float(actual_press, 1)      # kPa
        self.__sl_press = Datum.float(sl_press, 1)              # kPa

        self.__t_adc = Datum.int(t_adc)                         # T adc count
        self.__temp = Datum.float(temp, 1)                      # °C


    # ----------------------------------------------------------------------------------------------------------------

    def as_sample(self, tag, rec):
        return Sample(tag, None, rec, self.as_json())


    def as_json(self):
        jdict = OrderedDict()

        jdict['pA'] = self.actual_press

        if self.sl_press is not None:
            jdict['p0'] = self.sl_press

        if self.temp is not None:
            jdict['tmp'] = self.temp

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def c25(self, ref_temp):
        return MPL115A2Datum.__c25(ref_temp, self.__t_adc)


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


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MPL115A2Datum:{actual_press:%s, sl_press:%s, t_adc:%s, temp:%s}" % \
               (self.actual_press, self.sl_press, self.__t_adc, self.temp)
