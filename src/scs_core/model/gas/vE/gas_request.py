"""
Created on 2 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"sample": {"rec": "2021-10-15T09:14:38Z", "tag": "scs-be2-3", "ver": 1.0, "src": "AFE",
"val": {"NO2": {"weV": 0.29, "aeV": 0.29557, "weC": 0.0005, "cnc": 17.9, "vCal": 12.799},
"Ox": {"weV": 0.39951, "aeV": 0.39988, "weC": 0.00196, "cnc": 54.6, "vCal": 1.795, "xCal": -0.392451},
"CO": {"weV": 0.37994, "aeV": 0.28975, "weC": 0.09457, "cnc": 409.5, "vCal": 380.414},
"sht": {"hmd": 58.6, "tmp": 22.3}}}, "t-slope": -0.1, "rh-slope": 0.2, "brd-tmp": 32.5}
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

    def __init__(self, sample, t_slope, rh_slope, board_temp):
        """
        Constructor
        """
        self.__sample = sample                              # GasesSample (must contain EXT SHTDatum and vCal)

        self.__t_slope = float(t_slope)                     # float
        self.__rh_slope = float(rh_slope)                   # float
        self.__board_temp = float(board_temp)               # float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['sample'] = self.sample

        jdict['t-slope'] = self.t_slope
        jdict['rh-slope'] = self.rh_slope
        jdict['brd-tmp'] = self.board_temp

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
    def board_temp(self):
        return self.__board_temp


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GasRequest(vE):{sample:%s, t_slope:%s, rh_slope:%s, board_temp:%s}" %  \
               (self.sample, self.t_slope, self.rh_slope, self.board_temp)
