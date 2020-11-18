"""
Created on 14 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-be2-3", "src": "N3", "rec": "2019-12-10T15:24:04Z",
"val": {"per": 4.9, "pm1": 5.6, "pm2p5": 6.7, "pm10": 6.8,
"bin": [338, 42, 4, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
"mtf1": 83, "mtf3": 101, "mtf5": 0, "mtf7": 0, "sfr": 0.61,
"sht": {"hmd": 32.1, "tmp": 30.7}}}
"""

from collections import OrderedDict

from scs_core.data.str import Str

from scs_core.particulate.opc_datum import OPCDatum

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class ParticulatesSample(Sample):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # Sample...
        tag = jdict.get('tag')
        val = jdict.get('val')
        exegeses = jdict.get('exg')

        # ParticulatesSample...
        val['rec'] = jdict.get('rec')
        val['src'] = jdict.get('src')

        opc_datum = OPCDatum.construct_from_jdict(val)

        return cls(tag, opc_datum, exegeses=exegeses)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, opc_datum, exegeses=None):
        """
        Constructor
        """
        super().__init__(tag, opc_datum.rec, src=opc_datum.source, exegeses=exegeses)

        self.__opc_datum = opc_datum                                # OPCDatum


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def has_invalid_value(cls):
        # TODO: implement has_invalid_value
        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def values(self):
        jdict = OrderedDict()

        jdict['per'] = self.opc_datum.period

        jdict['pm1'] = self.opc_datum.pm1
        jdict['pm2p5'] = self.opc_datum.pm2p5
        jdict['pm10'] = self.opc_datum.pm10

        jdict['bin'] = self.opc_datum.bins

        jdict['mtf1'] = self.opc_datum.bin_1_mtof
        jdict['mtf3'] = self.opc_datum.bin_3_mtof
        jdict['mtf5'] = self.opc_datum.bin_5_mtof
        jdict['mtf7'] = self.opc_datum.bin_7_mtof

        if self.opc_datum.sfr is not None:
            jdict['sfr'] = self.opc_datum.sfr

        if self.opc_datum.sht is not None:
            jdict['sht'] = self.opc_datum.sht.as_json()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def opc_datum(self):
        return self.__opc_datum


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        exegeses = Str.collection(self.exegeses)

        return "ParticulatesSample:{tag:%s, rec:%s, src:%s, exegeses:%s, opc_datum:%s}" % \
            (self.tag, self.rec, self.src, exegeses, self.opc_datum)
