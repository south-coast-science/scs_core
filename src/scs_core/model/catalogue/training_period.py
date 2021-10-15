"""
Created on 22 Sep 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class TrainingPeriod(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, recs):
        start = min(recs)
        end = max(recs)

        return cls(start, end)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        start = LocalizedDatetime.construct_from_jdict(jdict.get('start'))
        end = LocalizedDatetime.construct_from_jdict(jdict.get('end'))

        return cls(start, end)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, start, end):
        """
        Constructor
        """
        self.__start = start                        # LocalizedDatetime
        self.__end = end                            # LocalizedDatetime


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def start(self):
        return self.__start


    @property
    def end(self):
        return self.__end


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['start'] = self.start
        jdict['end'] = self.end

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TrainingPeriod:{start:%s, end:%s}" % (self.start, self.end)
