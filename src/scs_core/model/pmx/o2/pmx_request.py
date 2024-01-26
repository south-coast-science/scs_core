"""
Created on 24 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"sample": {"rec": "2024-01-24T14:32:35Z", "tag": "scs-be2-3", "ver": 2.0, "src": "N3",
"val": {"per": 4.1, "pm1": 3.4, "pm2p5": 5.8, "pm10": 6.1,
"bin": [276, 175, 80, 13, 11, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
"mtf1": 27, "mtf3": 29, "mtf5": 40, "mtf7": 0, "sfr": 5.61,
"sht": {"hmd": 42.6, "tmp": 23.8}}},
"ext-sht": {"hmd": 46.6, "tmp": 24.9},
"slopes": {"ext-t": 0.1, "ext-rh": 0.2, "opc-t": 0.3, "opc-rh": 0.4}}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum

from scs_core.model.pmx.pmx_request import PMxRequest as AbstractPMxRequest


# --------------------------------------------------------------------------------------------------------------------

class PMxRequest(AbstractPMxRequest):
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

    def __init__(self, sample, sht_datum, ext_t_slope, ext_rh_slope, opc_t_slope, opc_rh_slope):
        """
        Constructor
        """
        self.__sample = sample                                                  # ParticulatesSample
        self.__sht_datum = sht_datum                                            # SHTDatum

        self.__ext_t_slope = Datum.float(ext_t_slope, ndigits=4)                # float or None
        self.__ext_rh_slope = Datum.float(ext_rh_slope, ndigits=4)              # float or None

        self.__opc_t_slope = Datum.float(opc_t_slope, ndigits=4)                # float or None
        self.__opc_rh_slope = Datum.float(opc_rh_slope, ndigits=4)              # float or None


    # ----------------------------------------------------------------------------------------------------------------

    def is_compatible(self, group):
        return self.sample.src == group.opc_version()


    def is_zero(self):
        return self.sample.opc_datum.is_zero()


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['sample'] = self.sample
        jdict['ext-sht'] = self.sht_datum

        jdict['slopes'] = {
            'ext-t': self.ext_t_slope,
            'ext-rh': self.ext_rh_slope,
            'opc-t': self.opc_t_slope,
            'opc-rh': self.opc_rh_slope
        }

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sample(self):
        return self.__sample


    @property
    def sht_datum(self):
        return self.__sht_datum


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
        return "PMxRequest(o2):{sample:%s, sht_datum:%s, ext_t_slope:%s, ext_rh_slope:%s, " \
               "opc_t_slope:%s, opc_rh_slope:%s}" %  \
               (self.sample, self.sht_datum, self.ext_t_slope, self.ext_rh_slope,
                self.opc_t_slope, self.opc_rh_slope)
