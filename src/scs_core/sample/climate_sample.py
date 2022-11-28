"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"rec": "2021-10-11T10:52:06Z", "tag": "scs-be2-3", "ver": 2.0, "val": {"hmd": 52.8, "tmp": 21.9,
"bar": {"pA": 103.5, "p0": 104.7}}}
"""

from collections import OrderedDict

from scs_core.climate.pressure_datum import PressureDatum
from scs_core.climate.sht_datum import SHTDatum

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.str import Str

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class ClimateSample(Sample):
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
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        try:
            version = round(float(jdict.get('ver')), 1)
        except (TypeError, ValueError):
            version = cls.DEFAULT_VERSION

        val = jdict.get('val')
        exegeses = jdict.get('exg')

        # ClimateSample...
        sht_datum = SHTDatum(val.get('hmd'), val.get('tmp'))

        node = val.get('bar')
        barometer_datum = None if node is None else PressureDatum(node.get('pA'), node.get('p0'), None)

        return cls(tag, rec, sht_datum, barometer_datum, version=version, exegeses=exegeses)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, sht_datum, barometer_datum, version=None, exegeses=None):
        """
        Constructor
        """
        if version is None:
            version = self.VERSION

        super().__init__(tag, rec, version, exegeses=exegeses)

        self.__sht_datum = sht_datum                                # SHT31Datum
        self.__barometer_datum = barometer_datum                    # PressureDatum


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def has_invalid_value(cls):
        # TODO: implement has_invalid_value
        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def values(self):
        jdict = OrderedDict()

        jdict['hmd'] = self.sht_datum.humid
        jdict['tmp'] = self.sht_datum.temp

        jdict['bar'] = self.barometer_datum

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sht_datum(self):
        return self.__sht_datum


    @property
    def barometer_datum(self):
        return self.__barometer_datum


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        exegeses = Str.collection(self.exegeses)

        return "ClimateSample:{tag:%s, rec:%s, exegeses:%s, sht_datum:%s, barometer_datum:%s}" % \
            (self.tag, self.rec, exegeses, self.sht_datum, self.barometer_datum)
