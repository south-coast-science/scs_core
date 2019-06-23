"""
Created on 11 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A JSONable extension to pytz.timezone.

https://stackoverflow.com/questions/13866926/python-pytz-list-of-timezones

example JSON:
{"name": "US/Michigan", "utc-offset": "-04:00"}
"""

import datetime
import pytz

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.location.timezone_offset import TimezoneOffset


# --------------------------------------------------------------------------------------------------------------------

class Timezone(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid(cls, name):
        return name in pytz.all_timezones


    @classmethod
    def zones(cls):
        return pytz.all_timezones


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        name = jdict.get('name')

        return Timezone(name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name):
        """
        Constructor
        """
        if not Timezone.is_valid(name):
            raise ValueError("Invalid timezone name: %s" % name)

        self.__name = name                              # a Pytz timezone name


    # ----------------------------------------------------------------------------------------------------------------

    def utc_offset(self, year, month, day, hour):
        tz = pytz.timezone(self.__name)
        dt = datetime.datetime(year=year, month=month, day=day, hour=hour)

        offset = tz.localize(dt).strftime('%z')

        return TimezoneOffset.construct_from_offset(offset)


    def current_utc_offset(self):
        if self.name is None:
            return None

        tz = pytz.timezone(self.name)
        dt = datetime.datetime.now(tz)

        offset = dt.strftime('%z')

        return TimezoneOffset.construct_from_offset(offset)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['name'] = self.name
        jdict['utc-offset'] = self.current_utc_offset()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def zone(self):
        return pytz.timezone(self.__name)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Timezone:{name:%s}" % self.name
