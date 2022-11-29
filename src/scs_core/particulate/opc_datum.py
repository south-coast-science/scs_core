"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.climate.sht_datum import SHTDatum

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum

from scs_core.particulate.pmx_datum import PMxDatum

from scs_core.sample.sample import Sample

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class OPCDatum(PMxDatum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        logger = Logging.getLogger()

        source = jdict.get('src')

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        period = jdict.get('per')

        pm1 = jdict.get('pm1')
        pm2p5 = jdict.get('pm2p5')
        pm10 = jdict.get('pm10')

        bins = jdict.get('bin')

        if bins is None:
            logger.error("OPCDatum incomplete: %s" % jdict)
            return None

        bin_1_mtof = jdict.get('mtf1')
        bin_3_mtof = jdict.get('mtf3')
        bin_5_mtof = jdict.get('mtf5')
        bin_7_mtof = jdict.get('mtf7')

        sfr = jdict.get('sfr')

        sht = SHTDatum.construct_from_jdict(jdict.get('sht'))

        return cls(source, rec, pm1, pm2p5, pm10, period, bins, bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof,
                   sfr=sfr, sht=sht)


    @classmethod
    def null_datum(cls):
        return cls(None, LocalizedDatetime.now().utc(), None, None, None, 0.0, [], 0, 0, 0, 0)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, source, rec, pm1, pm2p5, pm10, period, bins, bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof,
                 sfr=None, sht=None):
        """
        Constructor
        """
        PMxDatum.__init__(self, rec, pm1, pm2p5, None, pm10)

        self.__source = source                              # string

        self.__period = Datum.float(period, 1)              # seconds

        self.__bins = [int(count) for count in bins]        # array of count

        self.__bin_1_mtof = Datum.int(bin_1_mtof)           # float time
        self.__bin_3_mtof = Datum.int(bin_3_mtof)           # float time
        self.__bin_5_mtof = Datum.int(bin_5_mtof)           # float time
        self.__bin_7_mtof = Datum.int(bin_7_mtof)           # float time

        self.__sfr = Datum.float(sfr, 3)                    # float sample flow rate

        self.__sht = sht                                    # SHTDatum


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['src'] = self.source

        jdict['rec'] = None if self.rec is None else self.rec.as_iso8601(include_millis=Sample.INCLUDE_MILLIS)

        jdict['per'] = self.period

        jdict['pm1'] = self.pm1
        jdict['pm2p5'] = self.pm2p5
        jdict['pm10'] = self.pm10

        jdict['bin'] = self.bins

        jdict['mtf1'] = self.bin_1_mtof
        jdict['mtf3'] = self.bin_3_mtof
        jdict['mtf5'] = self.bin_5_mtof
        jdict['mtf7'] = self.bin_7_mtof

        jdict['sfr'] = self.sfr

        if self.sht is not None:
            jdict['sht'] = self.sht

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def is_zero(self):
        return self.pm1 == 0.0 and self.pm2p5 == 0.0 and self.pm10 == 0.0


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def source(self):
        return self.__source


    @property
    def period(self):
        return self.__period


    @property
    def bins(self):
        return self.__bins


    @property
    def bin_1_mtof(self):
        return self.__bin_1_mtof


    @property
    def bin_3_mtof(self):
        return self.__bin_3_mtof


    @property
    def bin_5_mtof(self):
        return self.__bin_5_mtof


    @property
    def bin_7_mtof(self):
        return self.__bin_7_mtof


    @property
    def sfr(self):
        return self.__sfr


    @property
    def sht(self):
        return self.__sht


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{source:%s, rec:%s, pm1:%s, pm2p5:%s, pm10:%s, period:%0.1f, bins:%s, " \
               "bin_1_mtof:%s, bin_3_mtof:%s, bin_5_mtof:%s, bin_7_mtof:%s, sfr:%s, sht:%s}" % \
               (self.source, self.rec, self.pm1, self.pm2p5, self.pm10, self.period, self.bins,
                self.bin_1_mtof, self.bin_3_mtof, self.bin_5_mtof, self.bin_7_mtof, self.sfr, self.sht)
