"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Text(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        pm1 = jdict.get('pm1')
        pm2p5 = jdict.get('pm2p5')
        pm10 = jdict.get('pm10')

        return cls(pm1, pm2p5, pm10)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pm1, pm2p5, pm10):
        """
        Constructor
        """
        self.__pm1 = Datum.float(pm1, 1)                # PM1
        self.__pm2p5 = Datum.float(pm2p5, 1)            # PM2.5
        self.__pm10 = Datum.float(pm10, 1)              # PM10


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['pm1'] = self.pm1
        jdict['pm2p5'] = self.pm2p5
        jdict['pm10'] = self.pm10

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def pm(self, species):
        if species == 'pm1':
            return self.__pm1

        if species == 'pm2p5':
            return self.__pm2p5

        if species == 'pm10':
            return self.__pm10

        raise ValueError(species)


    @property
    def pm1(self):
        return self.__pm1


    @property
    def pm2p5(self):
        return self.__pm2p5


    @property
    def pm10(self):
        return self.__pm10


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Text:{pm1:%s, pm2p5:%s, pm10:%s}" % (self.pm1, self.pm2p5, self.pm10)
