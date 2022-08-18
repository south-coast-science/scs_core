"""
Created on 17 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note: time shall always be represented as UTC, then localized on conversion.
"""

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import re

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class RTCDatetime(JSONable):
    """
    classdocs
    """

    CENTURY =               2000


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jstr(cls, jstr):
        if not jstr:
            return None

        match = re.match(r'(\d{2})-(\d{2})-(\d{2}) \((\d)\) (\d{2}):(\d{2}):(\d{2})', jstr)

        if match is None:
            return None

        fields = match.groups()

        # fields...
        year = int(fields[0])
        month = int(fields[1])
        day = int(fields[2])

        weekday = int(fields[3])

        hour = int(fields[4])
        minute = int(fields[5])
        second = int(fields[6])

        return cls(year, month, day, weekday, hour, minute, second)


    @classmethod
    def construct_from_localized_datetime(cls, localized_datetime):
        # RTC zone...
        zone_offset = timedelta()
        utc_zone = timezone(zone_offset)

        # localized...
        utc = localized_datetime.localize(utc_zone)
        rtc = utc.datetime

        # fields...
        year = rtc.year % 100
        month = rtc.month
        day = rtc.day

        weekday = rtc.isoweekday()

        hour = rtc.hour
        minute = rtc.minute
        second = rtc.second

        return cls(year, month, day, weekday, hour, minute, second)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, year, month, day, weekday, hour, minute, second):
        """
        Constructor
        """
        self.__year = year              # int       0 - 99
        self.__month = month            # int       1 - 12
        self.__day = day                # int       1 - 31

        self.__weekday = weekday        # int       1 - 7   ISO 8601: Monday is 1

        self.__hour = hour              # int       0 - 23
        self.__minute = minute          # int       0 - 59
        self.__second = second          # int       0 - 59


    # ----------------------------------------------------------------------------------------------------------------

    def as_localized_datetime(self, local_zone):        # may be pytz timezone or datetime timezone
        # RTC zone...
        zone_offset = timedelta()
        utc_zone = timezone(zone_offset)

        # localized...
        year = RTCDatetime.CENTURY + self.year

        rtc = datetime(year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second,
                       tzinfo=utc_zone)
        utc = LocalizedDatetime(rtc)

        # ...to host zone...
        localized = utc.localize(local_zone)

        return localized


    def as_json(self):
        return "%02d-%02d-%02d (%d) %02d:%02d:%02d" % \
               (self.year, self.month, self.day, self.weekday, self.hour, self.minute, self.second)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def year(self):
        return self.__year


    @property
    def month(self):
        return self.__month


    @property
    def day(self):
        return self.__day


    @property
    def weekday(self):
        return self.__weekday


    @property
    def hour(self):
        return self.__hour


    @property
    def minute(self):
        return self.__minute


    @property
    def second(self):
        return self.__second


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "RTCDatetime:{year:%s, month:%s, day:%s, weekday:%s, hour:%s, minute:%s, second:%s}" % \
               (self.year, self.month, self.day, self.weekday, self.hour, self.minute, self.second)
