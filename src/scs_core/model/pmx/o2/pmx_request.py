"""
Created on 24 Jan Dec 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"meteo-sample": {"rec": "2024-01-24T14:34:43Z", "tag": "scs-be2-3", "ver": 1.0,
"val": {"hmd": 46.6, "tmp": 24.9, "bar": null}},
"pmx-sample": {"rec": "2024-01-24T14:32:35Z", "tag": "scs-be2-3", "ver": 2.0, "src": "N3",
"val": {"per": 4.1, "pm1": 3.4, "pm2p5": 5.8, "pm10": 6.1,
"bin": [276, 175, 80, 13, 11, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
"mtf1": 27, "mtf3": 29, "mtf5": 40, "mtf7": 0, "sfr": 5.61,
"sht": {"hmd": 42.6, "tmp": 23.8}}},
"slopes": {"meteo-t": 0.1, "meteo-rh": 0.2, "opc-t": 0.3, "opc-rh": 0.4}}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PMxRequest(JSONable):
    """
    classdocs
    """

    __SLOPE_PERIOD = 900                # 15 minutes in seconds

    @classmethod
    def slope_tally(cls, schedule_duration):
        periods = int(round(cls.__SLOPE_PERIOD / schedule_duration))
        tally = 2 if periods < 2 else periods

        return tally


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pmx_sample, ext_sht_datum, ext_t_slope, ext_rh_slope, opc_t_slope, opc_rh_slope):
        """
        Constructor
        """
        self.__pmx_sample = pmx_sample                                          # ParticulatesSample
        self.__ext_sht_datum = ext_sht_datum                                    # SHTDatum

        self.__ext_t_slope = Datum.float(ext_t_slope, ndigits=4)                # float
        self.__ext_rh_slope = Datum.float(ext_rh_slope, ndigits=4)              # float

        self.__opc_t_slope = Datum.float(opc_t_slope, ndigits=4)                # float
        self.__opc_rh_slope = Datum.float(opc_rh_slope, ndigits=4)              # float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['pmx-sample'] = self.pmx_sample
        jdict['ext-sht'] = self.ext_sht_datum

        jdict['slopes'] = {
            'ext-t': self.ext_t_slope,
            'ext-rh': self.ext_rh_slope,
            'opc-t': self.opc_t_slope,
            'opc-rh': self.opc_rh_slope
        }

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pmx_sample(self):
        return self.__pmx_sample


    @property
    def ext_sht_datum(self):
        return self.__ext_sht_datum


    @property
    def ext_t_slope(self):
        return self.__ext_t_slope


    @property
    def ext_rh_slope(self):
        return self.__ext_rh_slope


    @property
    def opc_t_slope(self):
        return self.__opc_t_slope


    @property
    def opc_rh_slope(self):
        return self.__opc_rh_slope


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PMxRequest(o2):{pmx_sample:%s, ext_sht_datum:%s, " \
               "ext_t_slope:%s, ext_rh_slope:%s, opc_t_slope:%s, opc_rh_slope:%s}" %  \
               (self.pmx_sample, self.ext_sht_datum,
                self.ext_t_slope, self.ext_rh_slope, self.opc_t_slope, self.opc_rh_slope)
