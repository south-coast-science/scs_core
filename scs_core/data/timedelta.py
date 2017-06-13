"""
Created on 29 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A JSONable wrapper for timedelta.
"""

import re

from collections import OrderedDict
from datetime import timedelta

from scs_core.data.json import JSONable


# TODO: check whether we need to deal with weeks.

# --------------------------------------------------------------------------------------------------------------------

class Timedelta(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    "'0:00.37', '01-00:43:12'"

    @classmethod
    def construct_from_ps_time_report(cls, report):
        # uptime...
        match = re.match('(\d+)?(?::)?(\d+):(\d{2})(?:\.)?(\d{2})?', report)

        if match is None:
            return None

        fields = match.groups()
        # print(fields)

        hours = 0 if fields[0] is None else int(fields[0])
        minutes = int(fields[1])
        seconds = int(fields[2])
        milliseconds = 0 if fields[3] is None else int(fields[3]) * 10

        return Timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)


    @classmethod
    def construct_from_ps_elapsed_report(cls, report):
        # uptime...
        match = re.match('(\d+)?(?:-)?(\d{2})?(?::)?(\d{2}):(\d{2})', report)

        if match is None:
            return None

        fields = match.groups()
        # print(fields)

        days = 0 if fields[0] is None else int(fields[0])
        hours = 0 if fields[1] is None else int(fields[1])
        minutes = int(fields[2])
        seconds = int(fields[3])

        return Timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    " 12:32:26 up 21:19,  3 users,  load average: 0.00, 0.00, 0.00"

    "('21', None, None, '19')"

    @classmethod
    def construct_from_uptime_report(cls, report):
        # uptime...
        match = re.match('.*up (\d+)?\s*(min|day)?(?:s)?(?:,)?\s*(\d{1,2})?(?::)?(\d{1,2})?,', report)

        if match:
            fields = match.groups()

            print(fields)

            if fields[1] == 'min':
                return Timedelta(minutes=int(fields[0]))

            elif fields[1] == 'day':
                return Timedelta(days=int(fields[0]), hours=int(fields[2]), minutes=int(fields[3]))

            elif fields[1] is None:
                return Timedelta(hours=int(fields[0]), minutes=int(fields[3]))

            else:
                raise ValueError("unknown time unit: %s" % fields[1])

        else:
            return None


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        days = jdict.get('days')
        hours = jdict.get('hours')
        minutes = jdict.get('minutes')
        seconds = jdict.get('seconds')
        milliseconds = jdict.get('millis')

        return Timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, weeks=0, days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0):
        """
        Constructor
        """
        self.__td = timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds,
                              minutes=minutes, hours=hours, weeks=weeks)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['days'] = self.days

        jdict['hours'] = self.hours
        jdict['minutes'] = self.minutes
        jdict['seconds'] = self.seconds
        jdict['millis'] = self.milliseconds

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def delta(self):
        return self.__td


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def days(self):
        return self.__td.days


    @property
    def hours(self):
        return self.__td.seconds // 3600


    @property
    def minutes(self):
        return self.__td.seconds % 3600 // 60


    @property
    def seconds(self):
        return self.__td.seconds % 60


    @property
    def milliseconds(self):
        return self.__td.microseconds // 1000


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Timedelta:{%s}" % self.__td
