"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-ap1-6", "rec": "2019-01-22T13:55:54Z", "val": {"hmd": 49.3, "tmp": 21.5, "bar": {"pA": 99.8}}}
"""

from collections import OrderedDict

from scs_core.climate.pressure_datum import PressureDatum

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.str import Str

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class PressureSample(Sample):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))
        tag = jdict.get('tag')
        barometer_datum = PressureDatum.construct_from_jdict(jdict.get('val'))
        exegeses = jdict.get('exg')

        return cls(tag, rec, barometer_datum, exegeses=exegeses)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, barometer_datum, exegeses=None):
        """
        Constructor
        """
        super().__init__(tag, rec, exegeses=exegeses)

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

        jdict['bar'] = self.barometer_datum

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def barometer_datum(self):
        return self.__barometer_datum


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        exegeses = Str.collection(self.exegeses)

        return "PressureSample:{tag:%s, rec:%s, exegeses:%s, barometer_datum:%s}" % \
            (self.tag, self.rec, exegeses, self.barometer_datum)
