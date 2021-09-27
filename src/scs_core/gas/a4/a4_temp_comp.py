"""
Created on 22 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alphasense Application Note AAN 803-02
AAN 803-02 070916_DRAFT03.doc
"""

# import sys

from scs_core.gas.sensor import Sensor


# TODO: indicate with "alg" field to identify which equation is being used

# --------------------------------------------------------------------------------------------------------------------

class A4TempComp(object):
    """
    classdocs
    """

    __MIN_TEMP =        -30
    __MAX_TEMP =         50
    __INTERVAL =         10

    __COMP = None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):          # °C:                  -30   -20   -10    0    10    20    30    40    50
        cls.__COMP = {
            Sensor.CODE_CO:     A4TempComp(1, 'n_t', [1.0, 1.0, 1.0, 1.0, -0.2, -0.9, -1.5, -1.5, -1.5]),
            Sensor.CODE_H2S:    A4TempComp(1, 'n_t', [3.0, 3.0, 3.0, 1.0, -1.0, -2.0, -1.5, -1.0, -0.5]),
            Sensor.CODE_NO:     A4TempComp(3, 'kp_t', [0.7, 0.7, 0.7, 0.7, 0.8, 1.0, 1.2, 1.4, 1.6]),
            Sensor.CODE_NO2:    A4TempComp(1, 'n_t', [0.8, 0.8, 1.0, 1.2, 1.6, 1.8, 1.9, 2.5, 3.6]),
            Sensor.CODE_OX:     A4TempComp(3, 'kp_t', [0.1, 0.1, 0.2, 0.3, 0.7, 1.0, 1.7, 3.0, 4.0]),
            Sensor.CODE_SO2:    A4TempComp(1, 'kpp_t', [1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.9, 3.0, 5.8]),

            Sensor.CODE_VOCe:   A4TempComp(1, 'n_t', [1.0, 1.0, 1.0, 1.0, -0.2, -0.9, -1.5, -1.5, -1.5]),

            Sensor.CODE_TEST_1: None,
            Sensor.CODE_TEST_2: None,
            Sensor.CODE_TEST_3: None,
            Sensor.CODE_TEST_4: None
        }

        #   Recommended, but causes div by zero error if calib.ae_cal_mv is zero
        #   Sensor.CODE_H2S:    A4TempComp(2, 'k_t', [-1.5, -1.5, -1.5, -0.5, 0.5, 1.0, 0.8, 0.5, 0.3]),


    @classmethod
    def find(cls, sensor_code):
        if sensor_code not in cls.__COMP:
            raise ValueError("A4TempComp.find: unrecognised sensor code: %s." % sensor_code)

        return cls.__COMP[sensor_code]


    @classmethod
    def in_range(cls, temp):
        if temp is None:
            return False

        return temp <= cls.__MAX_TEMP


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, algorithm, factor, values):
        """
        Constructor
        """
        length = (A4TempComp.__MAX_TEMP - A4TempComp.__MIN_TEMP) // A4TempComp.__INTERVAL + 1

        if len(values) != length:
            raise ValueError("A4TempComp: value count should be %d." % length)

        self.__algorithm = algorithm        # int
        self.__factor = factor              # string
        self.__values = values              # array of float


    # ----------------------------------------------------------------------------------------------------------------

    def correct(self, calib, temp, we_t, ae_t):
        """
        Compute weC from weT, aeT
        """
        if not A4TempComp.in_range(temp):
            return None

        if self.__algorithm == 1:
            return self.__eq1(temp, we_t, ae_t)

        if self.__algorithm == 2:
            return self.__eq2(temp, we_t, ae_t, calib.we_cal_mv, calib.ae_cal_mv)

        if self.__algorithm == 3:
            return self.__eq3(temp, we_t, ae_t, calib.we_cal_mv, calib.ae_cal_mv)

        if self.__algorithm == 4:
            return self.__eq4(temp, we_t, calib.we_cal_mv)

        raise ValueError("A4TempComp.conv: unrecognised algorithm: %d." % self.__algorithm)


    # ----------------------------------------------------------------------------------------------------------------

    def __eq1(self, temp, we_t, ae_t):
        n_t = self.cf_t(temp)

        we_c = we_t - n_t * ae_t

        # print("A4TempComp.__eq1: alg:%d, temp:%f we_t:%f n_t:%f we_c:%f " %
        #       (self.__algorithm, temp, we_t, n_t, we_c), file=sys.stderr)

        return we_c


    def __eq2(self, temp, we_t, ae_t, we_cal_mv, ae_cal_mv):
        k_t = self.cf_t(temp)

        we_c = we_t - k_t * (we_cal_mv / ae_cal_mv) * ae_t

        # print("A4TempComp.__eq2: alg:%d, temp:%f we_t:%f ae_t:%f we_cal_mv:%f ae_cal_mv:%f k_t:%f we_c:%f " %
        #       (self.__algorithm, temp, we_t, ae_t, we_cal_mv, ae_cal_mv, k_t, we_c), file=sys.stderr)

        return we_c


    def __eq3(self, temp, we_t, ae_t, we_cal_mv, ae_cal_mv):
        kp_t = self.cf_t(temp)

        we_c = we_t - kp_t * (we_cal_mv - ae_cal_mv) * ae_t

        # print("A4TempComp.__eq3: alg:%d, temp:%f we_t:%f ae_t:%f we_cal_mv:%f ae_cal_mv:%f kp_t:%f we_c:%f " %
        #       (self.__algorithm, temp, we_t, ae_t, we_cal_mv, ae_cal_mv, kp_t, we_c), file=sys.stderr)

        return we_c


    def __eq4(self, temp, we_t, we_cal_mv):
        kpp_t = self.cf_t(temp)

        we_c = we_t - we_cal_mv - kpp_t

        # print("A4TempComp.__eq4: alg:%d, temp:%f we_t:%f we_cal_mv:%f kpp_t:%f we_c:%f " %
        #       (self.__algorithm, temp, we_t, we_cal_mv, kpp_t, we_c), file=sys.stderr)

        return we_c


    # ----------------------------------------------------------------------------------------------------------------

    def cf_t(self, temp):
        """
        Compute the linear-interpolated temperature compensation factor.
        """
        # below MIN_TEMP...
        if temp < A4TempComp.__MIN_TEMP:
            return self.__values[0]

        index = int((temp - A4TempComp.__MIN_TEMP) // A4TempComp.__INTERVAL)        # index of start of interval

        # on boundary...
        if temp % A4TempComp.__INTERVAL == 0:
            return self.__values[index]

        # all others...
        y1 = self.__values[index]                                                   # y value at start of interval
        y2 = self.__values[index + 1]                                               # y value at end of interval

        delta_y = y2 - y1

        delta_x = float(temp % A4TempComp.__INTERVAL) / A4TempComp.__INTERVAL       # proportion of interval

        cf_t = y1 + (delta_y * delta_x)

        # print("A4TempComp.cf_t: alg:%d, temp:%f y1:%f y2:%f delta_y:%f delta_x:%f cf_t:%f " %
        #       (self.__algorithm, temp, y1, y2, delta_y, delta_x, cf_t), file=sys.stderr)

        return cf_t


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def algorithm(self):
        return self.__algorithm


    @property
    def factor(self):
        return self.__factor


    @property
    def values(self):
        return self.__values


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4TempComp:{algorithm:%d, factor:%s, values:%s}" % (self.algorithm, self.factor, self.values)
