"""
Created on 14 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"rec": "2021-10-11T11:11:14Z", "tag": "scs-be2-3", "ver": 2.0, "src": "N3",
"val": {"per": 4.1, "pm1": 0.7, "pm2p5": 3.2, "pm10": 33.3,
"bin": [50, 24, 6, 2, 4, 2, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
"mtf1": 29, "mtf3": 32, "mtf5": 19, "mtf7": 54, "sfr": 3.73,
"sht": {"hmd": 43.6, "tmp": 25.6}},
"exg": {"src": "rn20", "val": {"pm1": 1.5, "pm2p5": 6.4, "pm10": 58.7}}}
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

    VERSION = 1.0

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        # Sample...
        tag = jdict.get('tag')

        try:
            version = round(float(jdict.get('ver')), 1)
        except (TypeError, ValueError):
            version = cls.DEFAULT_VERSION

        val = jdict.get('val')
        exegeses = jdict.get('exg')

        # ParticulatesSample...
        val['rec'] = jdict.get('rec')
        val['src'] = jdict.get('src')

        opc_datum = OPCDatum.construct_from_jdict(val)

        return cls(tag, opc_datum, version=version, exegeses=exegeses)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, opc_datum, version=None, exegeses=None):
        """
        Constructor
        """
        if version is None:
            version = self.VERSION

        super().__init__(tag, opc_datum.rec, version, src=opc_datum.source, exegeses=exegeses)

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
