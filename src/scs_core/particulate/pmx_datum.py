"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class PMxDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, pm1, pm2p5, pm4, pm10):
        """
        Constructor
        """
        self.__rec = rec                            # LocalizedDatetime

        self.__pm1 = Datum.float(pm1, 1)            # PM1
        self.__pm2p5 = Datum.float(pm2p5, 1)        # PM2.5
        self.__pm4 = Datum.float(pm4, 1)            # PM4
        self.__pm10 = Datum.float(pm10, 1)          # PM10


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec.as_iso8601(include_millis=Sample.INCLUDE_MILLIS)

        jdict['pm1'] = self.pm1
        jdict['pm2p5'] = self.pm2p5
        jdict['pm4'] = self.pm4
        jdict['pm10'] = self.pm10

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def pm1(self):
        return self.__pm1


    @property
    def pm2p5(self):
        return self.__pm2p5


    @property
    def pm4(self):
        return self.__pm4


    @property
    def pm10(self):
        return self.__pm10


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PMxDatum:{rec:%s, pm1:%s, pm2p5:%s, pm4:%s, pm10:%s}" % \
               (self.rec, self.pm1, self.pm2p5, self.pm4, self.pm10)
