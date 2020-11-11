"""
Created on 11 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class GasRequest(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sample, t_slope, rh_slope, sensor_calibs, calib_age):
        """
        Constructor
        """
        self.__sample = sample                              # Sample (gases)

        self.__t_slope = float(t_slope)                     # float
        self.__rh_slope = float(rh_slope)                   # float
        self.__sensor_calibs = sensor_calibs                # dict of gas_name: SensorCalib
        self.__calib_age = int(calib_age)                   # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['sample'] = self.sample.as_json()

        jdict['t-slope'] = self.t_slope
        jdict['rh-slope'] = self.rh_slope
        jdict['calibs'] = self.sensor_calibs
        jdict['calib-age'] = self.calib_age

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sample(self):
        return self.__sample


    @property
    def t_slope(self):
        return self.__t_slope


    @property
    def rh_slope(self):
        return self.__rh_slope


    @property
    def sensor_calibs(self):
        return self.__sensor_calibs


    @property
    def calib_age(self):
        return self.__calib_age


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        sensor_calibs = Str.collection(self.sensor_calibs)

        return "GasRequest:{sample:%s, t_slope:%s, rh_slope:%s, sensor_calibs:%s, calib_age:%s}" %  \
               (self.sample, self.t_slope, self.rh_slope, sensor_calibs, self.calib_age)
