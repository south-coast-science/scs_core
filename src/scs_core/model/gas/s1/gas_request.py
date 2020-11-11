"""
Created on 11 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

['ref.NO2 Processed Measurement (ppb)',
'praxis.meteo.val.tmp.cur', 'praxis.meteo.val.tmp.slope', 'praxis.meteo.val.hmd.cur', 'praxis.meteo.val.hmd.slope',
'praxis.gases.val.NO2.weV', 'praxis.gases.val.NO2.aeV',
'praxis.calib.sn1.we_electronic_zero_mv', 'praxis.calib.sn1.we_sensor_zero_mv', 'praxis.calib.sn1.we_total_zero_mv',
'praxis.calib.sn1.ae_electronic_zero_mv', 'praxis.calib.sn1.ae_sensor_zero_mv', 'praxis.calib.sn1.ae_total_zero_mv',
'praxis.calib.sn1.we_sensitivity_na_ppb', 'praxis.calib.sn1.we_cross_sensitivity_no2_na_ppb',
'praxis.calib.sn1.pcb_gain', 'praxis.calib.sn1.we_sensitivity_mv_ppb',
'praxis.calib-age']

example document:
"""

from collections import OrderedDict


# --------------------------------------------------------------------------------------------------------------------

class GasRequest(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sample, t_slope, rh_slope, calibs, calib_age):
        """
        Constructor
        """
        self.__sample = sample                              # Sample (gases)

        self.__t_slope = float(t_slope)                     # float
        self.__rh_slope = float(rh_slope)                   # float
        self.__calibs = calibs                              # dict of gas: calibration
        self.__calib_age = int(calib_age)                   # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['sample'] = self.sample.as_json()

        jdict['t-slope'] = self.t_slope
        jdict['rh-slope'] = self.rh_slope
        jdict['calibs'] = self.calibs.as_json()
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
    def calibs(self):
        return self.__calibs


    @property
    def calib_age(self):
        return self.__calib_age


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GasRequest:{sample:%s, t_slope:%s, rh_slope:%s, calibs:%s, calib_age:%s}" %  \
               (self.sample, self.t_slope, self.rh_slope, self.calibs, self.calib_age)
