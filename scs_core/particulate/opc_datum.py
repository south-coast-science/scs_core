"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.particulate.pmx_datum import PMxDatum


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

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        pm1 = jdict.get('pm1')
        pm2p5 = jdict.get('pm2p5')
        pm10 = jdict.get('pm10')

        period = jdict.get('per')

        bins = jdict.get('bin')

        bin_1_mtof = jdict.get('mtf1')
        bin_3_mtof = jdict.get('mtf3')
        bin_5_mtof = jdict.get('mtf5')
        bin_7_mtof = jdict.get('mtf7')

        return OPCDatum(rec, pm1, pm2p5, pm10, period, bins, bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, pm1, pm2p5, pm10, period, bins, bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof):
        """
        Constructor
        """
        PMxDatum.__init__(self, rec, pm1, pm2p5, pm10)

        self.__period = Datum.float(period, 1)              # seconds

        self.__bins = [int(count) for count in bins]        # array of count

        self.__bin_1_mtof = Datum.int(bin_1_mtof)           # time
        self.__bin_3_mtof = Datum.int(bin_3_mtof)           # time
        self.__bin_5_mtof = Datum.int(bin_5_mtof)           # time
        self.__bin_7_mtof = Datum.int(bin_7_mtof)           # time


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec.as_json()

        jdict['pm1'] = self.pm1
        jdict['pm2p5'] = self.pm2p5
        jdict['pm10'] = self.pm10

        jdict['per'] = self.period

        jdict['bin'] = self.bins

        jdict['mtf1'] = self.bin_1_mtof
        jdict['mtf3'] = self.bin_3_mtof
        jdict['mtf5'] = self.bin_5_mtof
        jdict['mtf7'] = self.bin_7_mtof

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

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


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCDatum:{rec:%s, pm1:%s, pm2p5:%s, pm10:%s, period:%0.1f, bins:%s, " \
               "bin_1_mtof:%s, bin_3_mtof:%s, bin_5_mtof:%s, bin_7_mtof:%s}" % \
                    (self.rec, self.pm1, self.pm2p5, self.pm10, self.period, self.bins,
                     self.bin_1_mtof, self.bin_3_mtof, self.bin_5_mtof, self.bin_7_mtof)
