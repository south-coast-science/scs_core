"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-ap1-6", "rec": "2019-01-22T13:55:54Z", "val": {"hmd": 49.3, "tmp": 21.5, "bar": {"pA": 99.8}}}
"""

from collections import OrderedDict

from scs_core.climate.mpl115a2_datum import MPL115A2Datum
from scs_core.climate.sht_datum import SHTDatum

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.str import Str

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class ClimateSample(Sample):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # Sample...
        tag = jdict.get('tag')
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))
        val = jdict.get('val')
        exegeses = jdict.get('exg')

        # ClimateSample...
        sht_datum = SHTDatum(val.get('hmd'), val.get('tmp'))

        node = val.get('bar')
        barometer_datum = None if node is None else MPL115A2Datum(node.get('pA'), node.get('p0'), None, None)

        return cls(tag, rec, sht_datum, barometer_datum, exegeses=exegeses)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, sht_datum, barometer_datum, exegeses=None):
        """
        Constructor
        """
        super().__init__(tag, rec, exegeses=exegeses)

        self.__sht_datum = sht_datum                                # SHT31Datum
        self.__barometer_datum = barometer_datum                    # MPL115A2Datum


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
