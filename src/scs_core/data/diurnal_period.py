"""
Created on 7 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/36414920/how-to-store-time-without-date-in-python-so-its-convenient-to-compare
https://en.wikipedia.org/wiki/Cron

document example:
{"type": "diurnal", "start": "09:00:00", "end": "17:00:00", "timezone": "Europe/London"}
"""

import pytz
import re

from collections import OrderedDict
from datetime import datetime, time

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.period import Period
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class DiurnalPeriod(Period, JSONable):
    """
    classdocs
    """

    __TYPE = 'diurnal'

    @classmethod
    def type(cls):
        return cls.__TYPE


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_time(cls, time_str):
        try:
            cls.__time(time_str)
            return True

        except ValueError:
            return False


    @classmethod
    def __time(cls, time_str):
        try:
            return time.fromisoformat(cls.__iso_time_str(time_str))
        except (TypeError, ValueError):
            raise ValueError(time_str)


    @classmethod
    def __iso_time_str(cls, time_str):
        if re.match(r'\d{2}:\d{2}:\d{2}', time_str):
            return time_str

        if re.match(r'\d{2}:\d{2}', time_str):
            return time_str + ':00'

        if re.match(r'\d:\d{2}', time_str):
            return '0' + time_str + ':00'

        raise ValueError(time_str)


    # ----------------------------------------------------------------------------------------------------------------

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


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, start_time: time, end_time: time, timezone: pytz.timezone):
        """
        Constructor
        """
        Period.__init__(self, timezone)

        self.__start_time = start_time                  # time
        self.__end_time = end_time                      # time


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


    def __contains__(self, point: LocalizedDatetime):
        localized_datetime = point.localize(self.timezone)
        localized_time = localized_datetime.datetime.time()

        return self.start_time <= localized_time < self.end_time


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.start_time != self.end_time


    def crosses_midnight(self):
        return self.start_time > self.end_time


    def has_expiring_dst(self):
        now = LocalizedDatetime.now().localize(self.timezone)
        tomorrow = (now + Timedelta(days=1)).localize(self.timezone)

        return now.dst() != tomorrow.dst()


    # ----------------------------------------------------------------------------------------------------------------

    def checkpoint(self):
        return str(self.end_datetime(LocalizedDatetime.now()).datetime.time())


    def cron(self, minutes_offset):
        return '%d %d * * *' % self.__cron_units(minutes_offset)


    def aws_cron(self, minutes_offset):
        return 'cron(%d %d * * ? *)' % self.__cron_units(minutes_offset)


    def __cron_units(self, minutes_offset):
        end_datetime = self.end_datetime(LocalizedDatetime.now())
        offset_end_datetime = (end_datetime + Timedelta(minutes=minutes_offset)).utc()
        dt = offset_end_datetime.datetime

        return dt.minute, dt.hour


    # ----------------------------------------------------------------------------------------------------------------

    def start_datetime(self, point: LocalizedDatetime):
        p_dt = point.datetime
        s_t = self.start_time

        start_dt = datetime(p_dt.year, month=p_dt.month, day=p_dt.day, hour=s_t.hour, minute=s_t.minute)
        start = LocalizedDatetime(self.timezone.localize(start_dt))

        if self.crosses_midnight():
            start -= Timedelta(days=1)

        return start


    def end_datetime(self, point: LocalizedDatetime):
        p_dt = point.datetime
        e_t = self.end_time

        end_dt = datetime(p_dt.year, month=p_dt.month, day=p_dt.day, hour=e_t.hour, minute=e_t.minute)
        end = LocalizedDatetime(self.timezone.localize(end_dt))

        return end


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, *args, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type()

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


    # ----------------------------------------------------------------------------------------------------------------

    def __repr__(self):
        return ' '.join((str(self.start_time), str(self.end_time), str(self.timezone)))


    def __str__(self, *args, **kwargs):
        return "DiurnalPeriod:{start_time:%s, end_time:%s, timezone:%s}" % \
            (self.start_time, self.end_time, self.timezone)
