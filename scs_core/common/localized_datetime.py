'''
Created on 13 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

import re

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import tzlocal

from scs_core.common.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class LocalizedDatetime(JSONable):
    '''
    classdocs
    '''

    @classmethod
    def now(cls):
        zone = tzlocal.get_localzone()
        localized = datetime.now(zone)

        return LocalizedDatetime(localized)


    @classmethod
    def construct_from_timestamp(cls, t):
        zone = tzlocal.get_localzone()
        localized = datetime.fromtimestamp(t, zone)

        return LocalizedDatetime(localized)


    @classmethod
    def construct_from_iso8601(cls, datetime_str):
        # numeric timezone offset...
        localized = cls.__construct_from_iso8601_z(datetime_str)

        if localized:
            return localized

        # Z timezone offset...
        return cls.__construct_from_iso8601_numeric(datetime_str)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __construct_from_iso8601_z(cls, datetime_str):
        # match...
        match = re.match('(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}).(\d{3})Z', datetime_str)

        if match is None:
            return None

        fields = match.groups()

        # fields...
        year = int(fields[0])
        month = int(fields[1])
        date = int(fields[2])

        hours = int(fields[3])
        mins = int(fields[4])
        secs = int(fields[5])
        micros = int(fields[6]) * 1000

        # construct...
        zone_offset = timedelta(hours=0, minutes=0)
        zone = timezone(zone_offset)

        localized = datetime(year, month, date, hours, mins, secs, micros, tzinfo=zone)

        return LocalizedDatetime(localized)


    @classmethod
    def __construct_from_iso8601_numeric(cls, datetime_str):
        # match...
        match = re.match('(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}).(\d{3})([+\-]?)(\d{2}):(\d{2})', datetime_str)

        if match is None:
            return None

        fields = match.groups()

        # fields...
        year = int(fields[0])
        month = int(fields[1])
        date = int(fields[2])

        hours = int(fields[3])
        mins = int(fields[4])
        secs = int(fields[5])
        micros = int(fields[6]) * 1000

        zone_sign = 1 if fields[7] == '+' else -1
        zone_hours = int(fields[8])
        zone_mins = int(fields[9])

        # construct...
        zone_offset = zone_sign * timedelta(hours=zone_hours, minutes=zone_mins)
        zone = timezone(zone_offset)

        localized = datetime(year, month, date, hours, mins, secs, micros, tzinfo=zone)

        return LocalizedDatetime(localized)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, localized):
        '''
        Constructor
        '''
        self.__localized = localized            # datetime


    def __add__(self, other: datetime):
        return LocalizedDatetime(self.__localized + other)


    def __sub__(self, other):
        other_datetime = other.__localized if type(other) == LocalizedDatetime else other

        return self.__localized - other_datetime


    # ----------------------------------------------------------------------------------------------------------------

    def as_iso8601(self):
        '''
        example: 2016-08-13T00:38:05.210+00:00
        '''
        date = self.__localized.strftime("%Y-%m-%d")
        time = self.__localized.strftime("%H:%M:%S")

        micros = float(self.__localized.strftime("%f"))
        frac = "%03d" % (micros // 1000)

        zone = self.__localized.strftime("%z")
        zone_hours = zone[:3]
        zone_mins = zone[3:]

        return "%sT%s.%s%s:%s" % (date, time, frac, zone_hours, zone_mins)


    def as_json(self):
        return self.as_iso8601()


    def timestamp(self):
        return self.__localized.timestamp()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def localized(self):
        return self.__localized


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LocalizedDatetime:{localized:%s}" % self.localized
