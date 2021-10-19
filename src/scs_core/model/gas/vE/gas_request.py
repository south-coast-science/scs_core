"""
Created on 2 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"sample": {"rec": "2021-10-19T08:36:34Z", "tag": "scs-be2-3", "ver": 1.0, "src": "AFE",
"val": {"NO2": {"weV": 0.28919, "aeV": 0.29607, "weC": -0.00125, "cnc": 11.3, "vCal": 7.91},
"Ox": {"weV": 0.39813, "aeV": 0.40013, "weC": 0.00286, "cnc": 57.1, "vCal": -2.849},
"CO": {"weV": 0.35688, "aeV": 0.29844, "weC": 0.08079, "cnc": 357.7, "vCal": 261.053},
"sht": {"hmd": 67.0, "tmp": 23.1}}},
"t-slope": 0.0, "rh-slope": 0.0, "brd-tmp": 28.6}
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
        self.__sample = sample                              # GasesSample (must contain EXT SHTDatum and vCals)

        self.__t_slope = float(t_slope)                     # float
        self.__rh_slope = float(rh_slope)                   # float
        self.__board_temp = float(board_temp)               # float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['sample'] = self.sample.as_json()

        jdict['tmp'] = {'cur': self.sample.sht_datum.temp, 'slope': self.t_slope, 'brd': self.board_temp}
        jdict['hmd'] = {'cur': self.sample.sht_datum.humid, 'slope': self.rh_slope}

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
