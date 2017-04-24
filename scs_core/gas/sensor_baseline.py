"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"calibrated_on": "2017-03-01", "offset": 444}
"""

from collections import OrderedDict

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

        calibrated_on = Datum.date(jdict.get('calibrated_on'))
        offset = Datum.int(jdict.get('offset'))

        return SensorBaseline(calibrated_on, offset)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calibrated_on, offset):
        """
        Constructor
        """
        self.__calibrated_on = calibrated_on            # date
        self.__offset = offset                          # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['calibrated_on'] = self.calibrated_on.isoformat() if self.calibrated_on else None
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
        return "SensorBaseline:{calibrated_on:%s, offset:%d}" % (self.calibrated_on, self.offset)
