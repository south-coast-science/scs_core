"""
Created on 13 Aug 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"particulates":
    {"tag": "scs-be2-3", "src": "N3", "rec": "2020-08-16T07:52:24Z",
    "val": {"per": 4.9, "pm1": 17.8, "pm2p5": 19.4, "pm10": 19.5,
    "bin": [703, 32, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "mtf1": 79, "mtf3": 80, "mtf5": 0, "mtf7": 0, "sfr": 0.52,
    "sht": {"hmd": 45.8, "tmp": 30.1}},
    "exg": {"ISLin/N3/vPLHR": {"pm1": 41.0, "pm2p5": 21.0, "pm10": 15.3}}},
"climate":
    {"hmd": 60.5, "tmp": 25.9}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PMxRequest(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sample, sht_datum):
        """
        Constructor
        """
        self.__sample = sample                              # ParticulatesSample
        self.__sht_datum = sht_datum                        # SHTDatum


    # ----------------------------------------------------------------------------------------------------------------

    def is_compatible(self, group):
        return self.sample.src == group.opc_version()


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['sample'] = self.sample.as_json()
        jdict['sht-datum'] = self.sht_datum.as_json()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sample(self):
        return self.__sample


    @property
    def sht_datum(self):
        return self.__sht_datum


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PMxRequest(s1):{sample:%s, sht_datum:%s}" %  (self.sample, self.sht_datum)
