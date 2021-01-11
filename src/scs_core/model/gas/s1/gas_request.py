"""
Created on 11 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"sample": {"tag": "test", "rec": "2020-11-11T16:16:34Z",
"val": {"NO2": {"weV": 0.31569, "aeV": 0.3095, "weC": 0.00395, "cnc": 11.6},
"CO": {"weV": 0.34176, "aeV": 0.25519, "weC": 0.09502, "cnc": 397.6},
"SO2": {"weV": 0.26657, "aeV": 0.26494, "weC": -0.00267, "cnc": 20.5},
"H2S": {"weV": 0.18319, "aeV": 0.26013, "weC": -0.04456, "cnc": 36.7},
"sht": {"hmd": 66.1, "tmp": 22.2}}},
"t-slope": 0.0, "rh-slope": 0.1,
"calib-age": 127109794}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class GasRequest(JSONable):
    """
    classdocs
    """

    __SLOPE_PERIOD = 900                # 15 minutes in seconds (was 300)

    @classmethod
    def slope_tally(cls, schedule_duration):
        periods = int(round(cls.__SLOPE_PERIOD / schedule_duration))
        tally = 2 if periods < 2 else periods

        return tally


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sample, t_slope, rh_slope, calib_age):
        """
        Constructor
        """
        self.__sample = sample                              # GasesSample (must contain EXT SHTDatum)

        self.__t_slope = float(t_slope)                     # float
        self.__rh_slope = float(rh_slope)                   # float
        self.__calib_age = int(calib_age)                   # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['sample'] = self.sample

        jdict['t-slope'] = self.t_slope
        jdict['rh-slope'] = self.rh_slope
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
    def calib_age(self):
        return self.__calib_age


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GasRequest(s1):{sample:%s, t_slope:%s, rh_slope:%s, calib_age:%s}" %  \
               (self.sample, self.t_slope, self.rh_slope, self.calib_age)
