"""
Created on 11 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A JSONable wrapper for datetime.strftime('%z').

https://stackoverflow.com/questions/5537876/get-utc-offset-from-time-zone-name-in-python

example JSON:
"-04:00"
"""

import re

from scs_core.data.json import JSONable
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class TimezoneOffset(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_offset(cls, offset):
        match = re.match(r'([+\-])(\d{2})(\d{2})', offset)

        if match is None:
            return None

        fields = match.groups()

        sign = -1 if fields[0] == '-' else 1

        hours = int(fields[1])
        minutes = int(fields[2])

        return TimezoneOffset(sign, hours, minutes)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sign, hours, minutes):
        """
        Constructor
        """
        self.__sign = sign                  # int { -1 or 1 }
        self.__hours = hours                # int
        self.__minutes = minutes            # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_timedelta(self):
        minutes = self.sign * ((self.hours * 60) + self.minutes)

        return Timedelta(minutes=minutes)


    def as_json(self):
        sign = '-' if self.sign < 0 else '+'

        return "%s%02d:%02d" % (sign, self.hours, self.minutes)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sign(self):
        return self.__sign


    @property
    def hours(self):
        return self.__hours


    @property
    def minutes(self):
        return self.__minutes


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TimezoneOffset:{sign:%d, hours:%02d, minutes:%02d}" % (self.sign, self.hours, self.minutes)
