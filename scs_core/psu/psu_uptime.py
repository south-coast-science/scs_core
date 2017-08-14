"""
Created on 8 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"secs": 57}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class PSUUptime(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        seconds = jdict.get('secs')

        return PSUUptime(seconds)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, seconds):
        """
        Constructor
        """
        self.__seconds = Datum.int(seconds)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['period'] = self.timedelta

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def seconds(self):
        return self.__seconds


    @property
    def timedelta(self):
        return Timedelta(seconds=self.seconds)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUUptime:{seconds:%s}" % self.seconds
