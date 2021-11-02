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
            return SensorBaseline(None, 0)

        if 'calibrated_on' in jdict:                            # TODO: deprecated
            date = Datum.date(jdict.get('calibrated_on'))
            calibrated_on = LocalizedDatetime.construct_from_date(date)

        else:
            calibrated_on = LocalizedDatetime.construct_from_iso8601(jdict.get('calibrated-on'))

        offset = jdict.get('offset')

        return SensorBaseline(calibrated_on, offset)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calibrated_on, offset):
        """
        Constructor
        """
        self.__calibrated_on = calibrated_on            # LocalizedDatetime

        self.__offset = int(offset)                     # int                       ppb


    def __eq__(self, other):
        try:
            return self.calibrated_on == other.calibrated_on and self.offset == other.offset
        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['calibrated-on'] = None if self.calibrated_on is None else self.calibrated_on.as_iso8601(False)
        jdict['offset'] = self.offset

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def calibrated_on(self):
        return self.__calibrated_on


    @property
    def offset(self):
        return self.__offset


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SensorBaseline:{calibrated_on:%s, offset:%s}" %  (self.calibrated_on, self.offset)
