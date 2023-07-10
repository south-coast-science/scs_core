"""
Created on 7 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/36414920/how-to-store-time-without-date-in-python-so-its-convenient-to-compare
"""

import pytz

from collections import OrderedDict
from datetime import time

from scs_core.data.json import JSONable
from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class Period(JSONable):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        return cls.construct(jdict.get('start'), jdict.get('end'), jdict.get('timezone'))


    @classmethod
    def construct(cls, start_time_str, end_time_str, timezone_str):
        start_time = cls.__time(start_time_str)
        end_time = cls.__time(end_time_str)

        if timezone_str not in pytz.all_timezones:
            raise ValueError(timezone_str)

        timezone = pytz.timezone(timezone_str)

        return cls(start_time, end_time, timezone)


    @classmethod
    def __time(cls, time_str):
        try:
            corrected_time_str = '0' + time_str if len(time_str) < 5 else time_str
            return time.fromisoformat(corrected_time_str + ':00')

        except (TypeError, ValueError):
            raise ValueError(time_str)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, start_time, end_time, timezone):
        """
        Constructor
        """
        self.__start_time = start_time                  # time
        self.__end_time = end_time                      # time
        self.__timezone = timezone                      # pytz.timezone


    def __lt__(self, other):
        if self.start_time < other.start_time:
            return True

        if self.start_time > other.start_time:
            return False

        if self.end_time < other.end_time:
            return True

        if self.end_time > other.end_time:
            return False

        return str(self.timezone) < str(other.timezone)


    def __contains__(self, datetime: LocalizedDatetime):
        localized_datetime = datetime.localize(self.timezone)
        localized_time = localized_datetime.datetime.time()

        return self.start_time <= localized_time < self.end_time


    # ----------------------------------------------------------------------------------------------------------------

    def has_valid_start_end(self):
        return self.start_time < self.end_time


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, *args, **kwargs):
        jdict = OrderedDict()

        jdict['start'] = str(self.start_time)
        jdict['end'] = str(self.end_time)
        jdict['timezone'] = str(self.timezone)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def start_time(self):
        return self.__start_time


    @property
    def end_time(self):
        return self.__end_time


    @property
    def timezone(self):
        return self.__timezone


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Period:{start_time:%s, end_time:%s, timezone:%s}" % (self.start_time, self.end_time, self.timezone)
