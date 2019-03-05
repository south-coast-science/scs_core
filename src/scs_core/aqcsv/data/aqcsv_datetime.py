"""
Created on 5 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import pytz
import re

from datetime import datetime, timedelta, timezone

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class AQCSVDatetime(JSONable):
    """
    classdocs
    """

    @classmethod
    def construct_from_jstr(cls, jstr):
        match = re.match('(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(([ +\-])(\d{2})(\d{2}))?', jstr)

        if match is None:
            return None

        fields = match.groups()

        # datetime...
        year = int(fields[0])
        month = int(fields[1])
        day = int(fields[2])

        hour = int(fields[3])
        minute = int(fields[4])

        # no zone...
        if fields[5] is None:
            utc_datetime = datetime(year, month, day, hour, minute, 0, 0)

            return AQCSVDatetime(utc_datetime, None)

        # zone...
        zone_sign = -1 if fields[6] == '-' else 1
        zone_hours = int(fields[7])
        zone_mins = int(fields[8])

        zone_offset = zone_sign * timedelta(hours=zone_hours, minutes=zone_mins)
        zone = timezone(zone_offset)

        localised_datetime = datetime(year, month, day, hour, minute, 0, 0, tzinfo=zone)

        return cls.construct_from_datetime(localised_datetime, zone)


    @classmethod
    def construct_from_datetime(cls, localised_datetime, zone):
        utc_datetime = localised_datetime.astimezone(pytz.timezone('Etc/UTC'))

        return AQCSVDatetime(utc_datetime, zone)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, utc_datetime, zone):
        """
        Constructor
        """
        self.__utc_datetime = utc_datetime
        self.__zone = zone


    def __hash__(self):
        return hash(self.utc_datetime)


    def __eq__(self, other):
        return self.utc_datetime == other.utc_datetime


    def __ge__(self, other):
        return self.utc_datetime >= other.utc_datetime


    def __gt__(self, other):
        return self.utc_datetime > other.utc_datetime


    def __le__(self, other):
        return self.utc_datetime <= other.utc_datetime


    def __lt__(self, other):
        return self.utc_datetime < other.utc_datetime


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        if self.zone is None:
            return self.utc_datetime.strftime("%Y%m%dT%H%M")

        localised = self.localised()

        return localised.strftime("%Y%m%dT%H%M%z")


    # ----------------------------------------------------------------------------------------------------------------

    def is_utc(self):
        return self.zone is None


    def localised(self):
        return self.utc_datetime.astimezone(self.__zone)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def utc_datetime(self):
        return self.__utc_datetime


    @property
    def zone(self):
        return self.__zone


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AQCSVDatetime:{utc_datetime:%s, zone:%s}" % (self.utc_datetime, self.zone)
