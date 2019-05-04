"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.climate.sht_datum import SHTDatum
from scs_core.particulate.pmx_datum import PMxDatum
from scs_core.sample.sample import Sample


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

        source = jdict.get('src')

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        period = jdict.get('per')

        pm1 = jdict.get('pm1')
        pm2p5 = jdict.get('pm2.5')
        pm10 = jdict.get('pm10')

        bins = jdict.get('bin')

        if bins is None:
            print("OPCDatum incomplete: %s" % jdict, file=sys.stderr)
            sys.stderr.flush()

            return None

        bin_1_mtof = jdict.get('mtf1')
        bin_3_mtof = jdict.get('mtf3')
        bin_5_mtof = jdict.get('mtf5')
        bin_7_mtof = jdict.get('mtf7')

        sht = SHTDatum.construct_from_jdict(jdict.get('sht'))

        return OPCDatum(source, rec, pm1, pm2p5, pm10, period, bins, bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof,
                        sht)


    @classmethod
    def null_datum(cls):
        return OPCDatum(None, LocalizedDatetime.now(), None, None, None, 0.0, [], 0, 0, 0, 0)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, source, rec, pm1, pm2p5, pm10, period, bins, bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof,
                 sht=None):
        """
        Constructor
        """
        PMxDatum.__init__(self, rec, pm1, pm2p5, None, pm10)

        self.__source = source                              # string

        self.__period = Datum.float(period, 1)              # seconds

        self.__bins = [int(count) for count in bins]        # array of count

        self.__bin_1_mtof = Datum.int(bin_1_mtof)           # time
        self.__bin_3_mtof = Datum.int(bin_3_mtof)           # time
        self.__bin_5_mtof = Datum.int(bin_5_mtof)           # time
        self.__bin_7_mtof = Datum.int(bin_7_mtof)           # time

        self.__sht = sht                                    # SHTDatum


    # ----------------------------------------------------------------------------------------------------------------

    def as_sample(self, tag):
        jdict = OrderedDict()

        jdict['per'] = self.period

        jdict['pm1'] = self.pm1
        jdict['pm2p5'] = self.pm2p5
        jdict['pm10'] = self.pm10

        jdict['bin'] = self.bins

        jdict['mtf1'] = self.bin_1_mtof
        jdict['mtf3'] = self.bin_3_mtof
        jdict['mtf5'] = self.bin_5_mtof
        jdict['mtf7'] = self.bin_7_mtof

        if self.sht is not None:
            jdict['sht'] = self.sht

        return Sample(tag, self.source, self.rec, jdict)


    def as_json(self):
        jdict = OrderedDict()

        jdict['src'] = self.source

        jdict['rec'] = self.rec.as_iso8601(Sample.INCLUDE_MILLIS)

        jdict['per'] = self.period

        jdict['pm1'] = self.pm1
        jdict['pm2p5'] = self.pm2p5
        jdict['pm10'] = self.pm10

        jdict['bin'] = self.bins

        jdict['mtf1'] = self.bin_1_mtof
        jdict['mtf3'] = self.bin_3_mtof
        jdict['mtf5'] = self.bin_5_mtof
        jdict['mtf7'] = self.bin_7_mtof

        if self.sht is not None:
            jdict['sht'] = self.sht

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def is_zero(self):
        return not self.pm1 and not self.pm2p5 and not self.pm10            # 0 or None


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
    def sht(self):
        return self.__sht


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCDatum:{source:%s, rec:%s, pm1:%s, pm2p5:%s, pm10:%s, period:%0.1f, bins:%s, " \
               "bin_1_mtof:%s, bin_3_mtof:%s, bin_5_mtof:%s, bin_7_mtof:%s, sht:%s}" % \
                    (self.source, self.rec, self.pm1, self.pm2p5, self.pm10, self.period, self.bins,
                     self.bin_1_mtof, self.bin_3_mtof, self.bin_5_mtof, self.bin_7_mtof, self.sht)
