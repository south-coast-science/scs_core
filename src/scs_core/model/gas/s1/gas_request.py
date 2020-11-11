"""
Created on 11 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"sample": {"tag": "test", "rec": "2020-11-11T16:16:34Z",
"val": {"NO2": {"weV": 0.31569, "aeV": 0.3095, "weC": 0.00395, "cnc": 11.6},
"CO": {"weV": 0.34176, "aeV": 0.25519, "weC": 0.09502, "cnc": 397.6},
"SO2": {"weV": 0.26657, "aeV": 0.26494, "weC": -0.00267, "cnc": 20.5},
"H2S": {"weV": 0.18319, "aeV": 0.26013, "weC": -0.04456, "cnc": 36.7},
"sht": {"hmd": 66.1, "tmp": 22.2}}}, "t-slope": 0.0, "rh-slope": 0.1,
"calibs": {"NO2": {"serial_number": "212060308", "sensor_type": "NO2A43F",
"we_electronic_zero_mv": 309, "we_sensor_zero_mv": 3, "we_total_zero_mv": 312,
"ae_electronic_zero_mv": 308, "ae_sensor_zero_mv": 1, "ae_total_zero_mv": 309,
"we_sensitivity_na_ppb": -0.264, "we_cross_sensitivity_no2_na_ppb": -0.264, "pcb_gain": -0.73,
"we_sensitivity_mv_ppb": 0.192, "we_cross_sensitivity_no2_mv_ppb": 0.192},
"CO": {"serial_number": "132950202", "sensor_type": "CO A4",
"we_electronic_zero_mv": 249, "we_sensor_zero_mv": 62, "we_total_zero_mv": 311,
"ae_electronic_zero_mv": 253, "ae_sensor_zero_mv": -1, "ae_total_zero_mv": 252,
"we_sensitivity_na_ppb": 0.299, "we_cross_sensitivity_no2_na_ppb": "n/a", "pcb_gain": 0.8,
"we_sensitivity_mv_ppb": 0.239, "we_cross_sensitivity_no2_mv_ppb": "n/a"},
"SO2": {"serial_number": "134060009", "sensor_type": "SO2A4",
"we_electronic_zero_mv": 266, "we_sensor_zero_mv": -1, "we_total_zero_mv": 265,
"ae_electronic_zero_mv": 263, "ae_sensor_zero_mv": 2, "ae_total_zero_mv": 265,
"we_sensitivity_na_ppb": 0.444, "we_cross_sensitivity_no2_na_ppb": "n/a", "pcb_gain": 0.8,
"we_sensitivity_mv_ppb": 0.355, "we_cross_sensitivity_no2_mv_ppb": "n/a"},
"H2S": {"serial_number": "133910023", "sensor_type": "H2SA4",
"we_electronic_zero_mv": 245, "we_sensor_zero_mv": -12, "we_total_zero_mv": 233,
"ae_electronic_zero_mv": 251, "ae_sensor_zero_mv": 13, "ae_total_zero_mv": 264,
"we_sensitivity_na_ppb": 1.782, "we_cross_sensitivity_no2_na_ppb": "n/a", "pcb_gain": 0.8,
"we_sensitivity_mv_ppb": 1.425, "we_cross_sensitivity_no2_mv_ppb": "n/a"}},
"calib-age": 127109794}
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
