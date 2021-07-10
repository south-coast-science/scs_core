"""
Created on 8 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Based-on code
https://invensense.tdk.com/download-pdf/icp-10101-datasheet/
"""

from scs_core.climate.pressure_datum import PressureDatum


# --------------------------------------------------------------------------------------------------------------------

class ICP10101Datum(PressureDatum):
    """
    TDK ICP-10101 digital barometer - data interpretation
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, actual_press, temp, altitude, include_temp=True):
        sl_press = cls._sl_press(actual_press, temp, altitude)
        reported_temp = temp if include_temp else None

        return cls(actual_press, sl_press, reported_temp)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, actual_press, sl_press, temp):
        """
        Constructor
        """
        super().__init__(actual_press, sl_press, temp)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ICP10101Datum:{actual_press:%s, sl_press:%s, temp:%s}" % \
               (self.actual_press, self.sl_press, self.temp)
