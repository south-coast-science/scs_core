"""
Created on 22 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

class PIDTempComp(object):
    """
    classdocs
    """

    __MIN_TEMP =        -30
    __MAX_TEMP =         70
    __INTERVAL =         10

    __COMP = None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):          # °C:               -30   -20   -10   0     10    20    30    40    50    60    70
        cls.__COMP = {
            Sensor.CODE_VOC_PPB_T1: PIDTempComp([1.35, 1.28, 1.21, 1.14, 1.07, 1.00, 0.96, 0.92, 0.88, 0.83, 0.79]),
            Sensor.CODE_VOC_PPB_T2: PIDTempComp([1.35, 1.28, 1.21, 1.14, 1.07, 1.00, 0.96, 0.92, 0.88, 0.83, 0.79]),
            Sensor.CODE_VOC_PPM: PIDTempComp([1.29, 1.24, 1.19, 1.13, 1.06, 1.00, 0.95, 0.90, 0.84, None, None]),
        }


    @classmethod
    def find(cls, sensor_code):
        if sensor_code not in cls.__COMP:
            raise ValueError("PIDTempComp.find: unrecognised sensor code: %s." % sensor_code)

        return cls.__COMP[sensor_code]


    @classmethod
    def in_range(cls, temp):
        if temp is None:
            return False

        return cls.__MIN_TEMP <= temp <= cls.__MAX_TEMP


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, values):
        """
        Constructor
        """
        length = (PIDTempComp.__MAX_TEMP - PIDTempComp.__MIN_TEMP) // PIDTempComp.__INTERVAL + 1

        if len(values) != length:
            raise ValueError("PIDTempComp: value count should be %d." % length)

        self.__values = values              # array of float


    # ----------------------------------------------------------------------------------------------------------------

    def correct(self, temp, we_t):
        """
        Compute weC from weT
        """
        if not PIDTempComp.in_range(temp):
            return None

        n_t = self.cf_t(temp)

        if n_t is None:
            return None

        we_c = we_t * n_t

        return we_c


    # ----------------------------------------------------------------------------------------------------------------

    def cf_t(self, temp):
        """
        Compute the linear-interpolated temperature compensation factor.
        """
        index = int((temp - PIDTempComp.__MIN_TEMP) // PIDTempComp.__INTERVAL)      # index of start of interval

        # on boundary...
        if temp % PIDTempComp.__INTERVAL == 0:
            return self.__values[index]

        # all others...
        y1 = self.__values[index]                                                   # y value at start of interval
        y2 = self.__values[index + 1]                                               # y value at end of interval

        if y1 is None or y2 is None:
            return None

        delta_y = y2 - y1

        delta_x = float(temp % PIDTempComp.__INTERVAL) / PIDTempComp.__INTERVAL     # proportion of interval

        cf_t = y1 + (delta_y * delta_x)

        return cf_t


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def values(self):
        return self.__values


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDTempComp:{values:%s}" % self.values
