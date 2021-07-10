"""
Created on 19 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Based-on code
https://github.com/hackscribble/microbit-MPL115A1-barometer/blob/master/microbit-MPL115A1-barometer.py
https://gist.github.com/cubapp/23dd4e91814a995b8ff06f406679abcf
"""

from scs_core.climate.pressure_datum import PressureDatum
from scs_core.data.datum import Datum


# --------------------------------------------------------------------------------------------------------------------

class MPL115A2Datum(PressureDatum):
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
    def __temp(cls, c25, t_adc):
        if c25 is None:
            return None

        return (t_adc - c25) / cls.__COUNTS_PER_DEGREE + 25.0


    @classmethod
    def __c25(cls, ref_temp, t_adc):
        return round(t_adc - cls.__COUNTS_PER_DEGREE * (ref_temp - 25.0))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, c25, p_comp, t_adc, altitude, include_temp=True):
        if p_comp is None or t_adc is None:
            return None

        temp = cls.__temp(c25, t_adc)

        actual_press = cls.__actual_press(p_comp)
        sl_press = cls._sl_press(actual_press, temp, altitude)

        reported_temp = temp if include_temp else None

        return cls(actual_press, sl_press, t_adc, reported_temp)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, actual_press, sl_press, t_adc, temp):
        """
        Constructor
        """
        super().__init__(actual_press, sl_press, temp)

        self.__t_adc = Datum.int(t_adc)                         # T adc count


    # ----------------------------------------------------------------------------------------------------------------

    def c25(self, ref_temp):
        return MPL115A2Datum.__c25(ref_temp, self.__t_adc)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MPL115A2Datum:{actual_press:%s, sl_press:%s, t_adc:%s, temp:%s}" % \
               (self.actual_press, self.sl_press, self.__t_adc, self.temp)
