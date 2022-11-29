"""
Created on 2 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable

from scs_core.particulate.pmx_datum import PMxDatum
from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class SPSDatum(PMxDatum):
    """
    classdocs
    """

    VERSION = 2.0

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        source = jdict.get('src')

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        pm1 = jdict.get('pm1')
        pm2p5 = jdict.get('pm2p5')
        pm4 = jdict.get('pm4')
        pm10 = jdict.get('pm10')

        counts = SPSDatumCounts.construct_from_jdict(jdict.get('counts'))
        tps = jdict.get('tps')

        return cls(source, rec, pm1, pm2p5, pm4, pm10, counts, tps)


    @classmethod
    def null_datum(cls):
        return cls(None, LocalizedDatetime.now().utc(), None, None, None, None, [], None)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, source, rec, pm1, pm2p5, pm4, pm10, counts, tps):
        """
        Constructor
        """
        PMxDatum.__init__(self, rec, pm1, pm2p5, pm4, pm10)

        self.__source = source                                      # string

        self.__counts = counts                                      # SPSDatumCounts
        self.__tps = Datum.float(tps, 3)                            # typical particle size


    # ----------------------------------------------------------------------------------------------------------------

    def as_sample(self, tag):                           # TODO: remove as_sample(..)
        jdict = OrderedDict()

        jdict['pm1'] = self.pm1
        jdict['pm2p5'] = self.pm2p5
        jdict['pm4'] = self.pm4
        jdict['pm10'] = self.pm10

        jdict['counts'] = self.counts
        jdict['tps'] = self.tps

        return Sample(tag, self.rec, self.VERSION, src=self.source, values=jdict)


    def as_json(self):
        jdict = OrderedDict()

        jdict['src'] = self.source

        jdict['rec'] = self.rec.as_iso8601(include_millis=Sample.INCLUDE_MILLIS)

        jdict['pm1'] = self.pm1
        jdict['pm2p5'] = self.pm2p5
        jdict['pm4'] = self.pm4
        jdict['pm10'] = self.pm10

        jdict['counts'] = self.counts
        jdict['tps'] = self.tps

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def is_zero(self):
        return not self.pm1 and not self.pm2p5 and not self.pm4 and not self.pm10            # 0 or None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def source(self):
        return self.__source


    @property
    def counts(self):
        return self.__counts


    @property
    def tps(self):
        return self.__tps


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SPSDatum:{source:%s, rec:%s, pm1:%s, pm2p5:%s, pm4:%s, pm10:%s, counts:%s, tps:%s}" % \
                    (self.source, self.rec, self.pm1, self.pm2p5, self.pm4, self.pm10, self.counts, self.tps)


# --------------------------------------------------------------------------------------------------------------------

class SPSDatumCounts(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        pm0p5 = jdict.get('pm0p5')
        pm1 = jdict.get('pm1')
        pm2p5 = jdict.get('pm2p5')
        pm4 = jdict.get('pm4')
        pm10 = jdict.get('pm10')

        return cls(pm0p5, pm1, pm2p5, pm4, pm10)


    @classmethod
    def null_datum(cls):
        return cls(None, None, None, None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pm0p5, pm1, pm2p5, pm4, pm10):
        """
        Constructor
        """
        self.__pm0p5 = int(round(pm0p5))                    # PM0.5
        self.__pm1 = int(round(pm1))                        # PM1
        self.__pm2p5 = int(round(pm2p5))                    # PM2.5
        self.__pm4 = int(round(pm4))                        # PM4
        self.__pm10 = int(round(pm10))                      # PM10


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['pm0p5'] = self.pm0p5
        jdict['pm1'] = self.pm1
        jdict['pm2p5'] = self.pm2p5
        jdict['pm4'] = self.pm4
        jdict['pm10'] = self.pm10

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def is_zero(self):
        return not self.pm0p5 and not self.pm1 and not self.pm2p5 and not self.pm4 and not self.pm10    # 0 or None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pm0p5(self):
        return self.__pm0p5


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
        return "SPSDatumCounts:{pm0p5:%s, pm1:%s, pm2p5:%s, pm4:%s, pm10:%s}" % \
                    (self.pm0p5, self.pm1, self.pm2p5, self.pm4, self.pm10)
