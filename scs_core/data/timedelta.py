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

        hours = 0 if fields[0] is None else int(fields[0])
        minutes = int(fields[1])
        seconds = int(fields[2])
        milliseconds = 0 if fields[3] is None else int(fields[3]) * 10

        return Timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)


    @classmethod
    def construct_from_ps_elapsed_report(cls, report):
        # uptime...
        match = re.match('(\d+)?(-)?(\d{2})?(?::)?(\d{2}):(\d{2})', report)

        if match is None:
            return None

        fields = match.groups()

        if fields[1] == "-":
            days = int(fields[0])
            hours = 0 if fields[2] is None else int(fields[2])
        else:
            days = 0
            hours = 0 if fields[0] is None else int(fields[0])

        minutes = int(fields[3])
        seconds = int(fields[4])

        return Timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


    @classmethod
    def construct_from_uptime_report(cls, report):
        # uptime...
        #                       0        1                    2        3                    4               5
        match = re.match('.*up (\d+)?\s*(day)?(?:s)?(?:,)?\s*(\d+)?\s*(min)?(?:s)?(?:,)?\s*(\d{1,2})?(?::)?(\d{1,2})?,',
                         report)

        if match:
            fields = match.groups()

            print(report)
            print(fields)

            if fields[1] == 'day':
                days = int(fields[0])
                minutes = int(fields[2]) if fields[3] == 'min' else int(fields[5])

            else:
                days = 0
                minutes = int(fields[0]) if fields[3] == 'min' else int(fields[5])

            hours = 0 if fields[3] == 'min' else int(fields[0])

            return Timedelta(days=days, hours=hours, minutes=minutes)


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
