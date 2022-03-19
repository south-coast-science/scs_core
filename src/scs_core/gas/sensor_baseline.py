"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"calibrated-on": "2019-02-02T11:34:16Z", "offset": 50}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SensorBaseline(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return cls.null_datum()

        if 'calibrated_on' in jdict:                            # TODO: deprecated
            date = Datum.date(jdict.get('calibrated_on'))
            calibrated_on = LocalizedDatetime.construct_from_date(date)

        else:
            calibrated_on = LocalizedDatetime.construct_from_iso8601(jdict.get('calibrated-on'))

        sample_on = LocalizedDatetime.construct_from_iso8601(jdict.get('sample-on'))
        sample_humid = jdict.get('sample-hmd')
        sample_temp = jdict.get('sample-tmp')

        offset = jdict.get('offset')

        return SensorBaseline(calibrated_on, sample_on, sample_humid, sample_temp, offset)


    @classmethod
    def null_datum(cls):
        return SensorBaseline(None, None, None, None, 0)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calibrated_on, sample_on, sample_humid, sample_temp, offset):
        """
        Constructor
        """
        self.__calibrated_on = calibrated_on                    # LocalizedDatetime

        self.__sample_on = sample_on                            # LocalizedDatetime
        self.__sample_humid = Datum.float(sample_humid, 1)      # float
        self.__sample_temp = Datum.float(sample_temp, 1)        # float

        self.__offset = int(offset)                             # int                       ppb


    def __eq__(self, other):
        try:
            return self.calibrated_on == other.calibrated_on and self.sample_on == other.sample_on and \
                   self.sample_humid == other.sample_humid and self.sample_temp == other.sample_temp and \
                   self.offset == other.offset
        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['calibrated-on'] = None if self.calibrated_on is None else self.calibrated_on.as_iso8601(False)

        jdict['sample-on'] = None if self.sample_on is None else self.sample_on.as_iso8601(False)
        jdict['sample-hmd'] = self.sample_humid
        jdict['sample-tmp'] = self.sample_temp

        jdict['offset'] = self.offset

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def calibrated_on(self):
        return self.__calibrated_on


    @property
    def sample_on(self):
        return self.__sample_on


    @property
    def sample_humid(self):
        return self.__sample_humid


    @property
    def sample_temp(self):
        return self.__sample_temp


    @property
    def offset(self):
        return self.__offset


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SensorBaseline:{calibrated_on:%s, sample_on:%s, sample_humid:%s, sample_temp:%s, offset:%s}" %  \
               (self.calibrated_on, self.sample_on, self.sample_humid, self.sample_temp, self.offset)
