"""
Created on 2 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"sample": {"rec": "2021-10-19T11:20:37Z", "tag": "scs-be2-3", "ver": 1.0, "src": "AFE",
"val": {
"NO2": {"weV": 0.28882, "aeV": 0.29582, "weC": -0.00118, "cnc": 11.6, "vCal": 7.463},
"Ox": {"weV": 0.39938, "aeV": 0.39982, "weC": 0.0037, "cnc": 59.6, "vCal": 1.595},
"CO": {"weV": 0.34707, "aeV": 0.30013, "weC": 0.07294, "cnc": 328.2, "vCal": 217.82},
"sht": {"hmd": 65.8, "tmp": 23.4}}},
"tmp": {"cur": 23.4, "slope": 0.0, "brd": 28.8},
"hmd": {"cur": 65.8, "slope": 0.0}}

example document (preprocessed):
{"sample": {"rec": "2021-10-19T11:18:16Z", "tag": "scs-be2-3", "ver": 1.0, "src": "AFE",
"val": {
"NO2": {"weV": 0.28869, "aeV": 0.296, "weC": -0.00165, "cnc": 9.8, "vCalOrig": 6.306, "vCal": "6.306", "vCalExtr": "0"},
"Ox": {"weV": 0.39944, "aeV": 0.39969, "weC": 0.0041, "cnc": 60.7, "vCal": 2.137},
"CO": {"weV": 0.34544, "aeV": 0.29738, "weC": 0.06828, "cnc": 310.7, "vCal": 222.03},
"sht": {"hmd": 65.8, "tmp": 23.4}}},
"tmp": {"curOrig": 23.4, "cur": "23.4", "slopeOrig": 0.0, "slope": "0", "brdOrig": 28.8, "brd": "28.8"},
"hmd": {"curOrig": 65.8, "cur": "65.8", "slopeOrig": 0.0, "slope": "0"}}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
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
        self.__sample = sample                                      # GasesSample (must contain EXT SHTDatum and vCals)

        self.__t_slope = Datum.float(t_slope, ndigits=4)            # float
        self.__rh_slope = Datum.float(rh_slope, ndigits=4)          # float
        self.__board_temp = Datum.float(board_temp, ndigits=1)      # float


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
