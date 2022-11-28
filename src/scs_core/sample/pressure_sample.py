"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"rec": "2021-10-11T11:08:24Z", "tag": "scs-be2-3", "ver": 2.0,
"val": {"bar": {"pA": 103.5, "p0": 104.7, "tmp": 22.6}}}
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

    VERSION = 1.0

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        tag = jdict.get('tag')
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        try:
            version = round(float(jdict.get('ver')), 1)
        except (TypeError, ValueError):
            version = cls.DEFAULT_VERSION

        barometer_datum = PressureDatum.construct_from_jdict(jdict.get('val'))
        exegeses = jdict.get('exg')

        return cls(tag, rec, barometer_datum, version=version, exegeses=exegeses)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, barometer_datum, version=None, exegeses=None):
        """
        Constructor
        """
        if version is None:
            version = self.VERSION

        super().__init__(tag, rec, version, exegeses=exegeses)

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
