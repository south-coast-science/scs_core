"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"calibrated-on": "2021-06-02T13:11:31+01:00", "offset": -123,
"sample": {"rec": "2021-06-01T13:11:31+01:00", "hmd": 54.3, "tmp": 12.3}}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable
from scs_core.data.path_dict import PathDict


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

        if 'calibrated_on' in jdict:
            date = Datum.date(jdict.get('calibrated_on'))                   # deprecated
            calibrated_on = LocalizedDatetime.construct_from_date(date)

        else:
            calibrated_on = LocalizedDatetime.construct_from_iso8601(jdict.get('calibrated-on'))

        offset = jdict.get('offset')
        sample = SensorBaselineSample.construct_from_jdict(jdict.get('env'))

        return cls(calibrated_on, offset, sample=sample)


    @classmethod
    def null_datum(cls):
        return cls(None, 0)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calibrated_on, offset, sample=None):
        """
        Constructor
        """
        self.__calibrated_on = calibrated_on                    # LocalizedDatetime
        self.__offset = int(offset)                             # int                           ppb
        self.__sample = sample                                  # SensorBaselineSample


    def __eq__(self, other):
        try:
            return self.calibrated_on == other.calibrated_on and self.offset == other.offset and \
                   self.sample == other.sample
        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['calibrated-on'] = None if self.calibrated_on is None else self.calibrated_on.as_iso8601()
        jdict['offset'] = self.offset

        if self.sample is not None:
            jdict['env'] = self.sample

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def calibrated_on(self):
        return self.__calibrated_on


    @property
    def offset(self):
        return self.__offset


    @property
    def sample(self):
        return self.__sample


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SensorBaseline:{calibrated_on:%s, offset:%s, sample:%s}" %  \
               (self.calibrated_on, self.offset, self.sample)


# --------------------------------------------------------------------------------------------------------------------

class SensorBaselineSample(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        humid = jdict.get('hmd')
        temp = jdict.get('tmp')
        press = jdict.get('pA')

        return cls(rec, humid, temp, press)


    @classmethod
    def construct_from_sample_jdict(cls, jdict):
        if not jdict:
            return None

        sample = PathDict(jdict)

        rec = LocalizedDatetime.construct_from_iso8601(sample.node('rec'))
        humid = sample.node('val.sht.hmd')
        temp = sample.node('val.sht.tmp')
        press = sample.node('val.sht.bar.pA') if sample.has_path('val.sht.bar') else None

        return cls(rec, humid, temp, press)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, humid, temp, press):
        """
        Constructor
        """
        self.__rec = rec                                # LocalizedDatetime
        self.__humid = Datum.float(humid, 1)            # float
        self.__temp = Datum.float(temp, 1)              # float
        self.__press = Datum.float(press, 1)            # float


    def __eq__(self, other):
        try:
            return self.rec == other.rec and self.humid == other.humid and self.temp == other.temp and \
                   self.press == other.press
        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.rec is not None:
            jdict['rec'] = self.rec.as_iso8601()

        jdict['hmd'] = self.humid
        jdict['tmp'] = self.temp

        if self.press is not None:
            jdict['pA'] = self.press

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def humid(self):
        return self.__humid


    @property
    def temp(self):
        return self.__temp


    @property
    def press(self):
        return self.__press


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SensorBaselineSample:{rec:%s, humid:%s, temp:%s, press:%s}" %  \
               (self.rec, self.humid, self.temp, self.press)
