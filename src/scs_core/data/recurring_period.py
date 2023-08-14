"""
Created on 7 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
https://en.wikipedia.org/wiki/Cron

document example:
{"type": "recurring", "interval": 1, "units": "D", "timezone": "Europe/London"}
"""

import pytz

from abc import abstractmethod
from collections import OrderedDict
from datetime import datetime

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.period import Period
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class RecurringPeriod(Period, JSONable):
    """
    classdocs
    """
    _UTC = pytz.timezone('Etc/UTC')

    __TYPE = 'recurring'

    @classmethod
    def type(cls):
        return cls.__TYPE


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def valid_intervals(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, timezone=None):
        if not jdict:
            return None

        interval = jdict.get('interval')
        units = jdict.get('units')
        timezone_str = jdict.get('timezone', timezone)

        return cls.construct(interval, units, timezone_str)


    @classmethod
    def construct(cls, interval, units, timezone_str):
        timezone = pytz.timezone(timezone_str)

        if units == 'D':
            return RecurringDay(interval, timezone)

        if units == 'H':
            return RecurringHours(interval, timezone)

        if units == 'M':
            return RecurringMinutes(interval, timezone)

        raise ValueError(units)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interval, timezone: pytz.timezone):
        """
        Constructor
        """
        Period.__init__(self, timezone)

        self.__interval = int(interval)                                             # int


    @abstractmethod
    def __lt__(self, other):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def _cron_minutes(self, minutes_offset):
        utc_now = LocalizedDatetime.now().utc()
        local_now = utc_now.localize(self.timezone)
        cron_minutes = (abs(local_now.datetime.minute - utc_now.datetime.minute) + minutes_offset) % 60

        return cron_minutes


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def timedelta(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def has_expiring_dst(self):
        return False


    # ----------------------------------------------------------------------------------------------------------------

    def start_datetime(self, point: LocalizedDatetime):
        return self.end_datetime(point) - self.timedelta()


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['type'] = self.type()

        jdict['interval'] = self.interval
        jdict['units'] = self.units
        jdict['timezone'] = str(self.timezone)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def interval(self):
        return self.__interval


    @property
    @abstractmethod
    def units(self):
        pass


    @property
    @abstractmethod
    def repr_units(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __repr__(self):
        return ' '.join((str(self.interval), self.repr_units))


    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{interval:%s, timezone:%s}" %  (self.interval, self.timezone)


# --------------------------------------------------------------------------------------------------------------------

class RecurringDay(RecurringPeriod):
    """
    classdocs
    """

    @classmethod
    def valid_intervals(cls):
        return 1,


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interval, timezone: pytz.timezone):
        """
        Constructor
        """
        super().__init__(interval, timezone)


    def __lt__(self, other):
        if isinstance(other, RecurringHours) or isinstance(other, RecurringMinutes):
            return False

        return self.interval < other.interval


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.interval == 1


    def checkpoint(self):
        return '00:00:00'


    def cron(self, minutes_offset):
        return '%d 0 * * *' % self._cron_minutes(minutes_offset)


    def aws_cron(self, minutes_offset):
        return 'cron(%d 0 * * ? *)' % self._cron_minutes(minutes_offset)


    def timedelta(self):
        return Timedelta(days=self.interval)


    def end_datetime(self, origin: LocalizedDatetime):
        dt = origin.utc().datetime

        return LocalizedDatetime(datetime(dt.year, month=dt.month, day=dt.day, tzinfo=self._UTC))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def units(self):
        return 'D'


    @property
    def repr_units(self):
        return 'day' if self.interval == 1 else 'days'


# --------------------------------------------------------------------------------------------------------------------

class RecurringHours(RecurringPeriod):
    """
    classdocs
    """

    __DIVISORS = (1, 2, 3, 4, 6, 8, 12)

    @classmethod
    def valid_intervals(cls):
        return cls.__DIVISORS


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interval, timezone: pytz.timezone):
        """
        Constructor
        """
        super().__init__(interval, timezone)


    def __lt__(self, other):
        if isinstance(other, RecurringDay):
            return True

        if isinstance(other, RecurringMinutes):
            return False

        return self.interval < other.interval


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.interval in self.__DIVISORS


    def checkpoint(self):
        return '/%d:00:00' % self.interval


    # ----------------------------------------------------------------------------------------------------------------

    def cron(self, minutes_offset):
        return '%d */%d * * *' % (self._cron_minutes(minutes_offset), self.interval)


    def aws_cron(self, minutes_offset):
        return 'cron(%d 0/%d * * ? *)' % (self._cron_minutes(minutes_offset), self.interval)


    # ----------------------------------------------------------------------------------------------------------------


    def timedelta(self):
        return Timedelta(hours=self.interval)


    def end_datetime(self, origin: LocalizedDatetime):
        dt = origin.utc().datetime
        hour = (dt.hour // self.interval) * self.interval

        return LocalizedDatetime(datetime(dt.year, month=dt.month, day=dt.day, hour=hour, tzinfo=self._UTC))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def units(self):
        return 'H'


    @property
    def repr_units(self):
        return 'hour' if self.interval == 1 else 'hours'


# --------------------------------------------------------------------------------------------------------------------

class RecurringMinutes(RecurringPeriod):
    """
    classdocs
    """

    __DIVISORS = (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30)

    @classmethod
    def valid_intervals(cls):
        return cls.__DIVISORS


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interval, timezone: pytz.timezone):
        """
        Constructor
        """
        super().__init__(interval, timezone)


    def __lt__(self, other):
        if isinstance(other, RecurringDay) or isinstance(other, RecurringHours):
            return True

        return self.interval < other.interval


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.interval in self.__DIVISORS


    def checkpoint(self):
        return '**:/%d:00' % self.interval


    def cron(self, minutes_offset):
        minutes = [str(minute + minutes_offset) for minute in range(0, 60, self.interval)]

        return '%s * * * *' % ','.join(minutes)


    def aws_cron(self, minutes_offset):
        minutes = '/'.join((str(minutes_offset), str(self.interval)))

        return 'cron(%s * * * ? *)' % minutes


    def timedelta(self):
        return Timedelta(minutes=self.interval)


    def end_datetime(self, origin: LocalizedDatetime):
        dt = origin.utc().datetime
        minute = (dt.minute // self.interval) * self.interval

        return LocalizedDatetime(datetime(dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=minute,
                                          tzinfo=self._UTC))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def units(self):
        return 'M'


    @property
    def repr_units(self):
        return 'minute' if self.interval == 1 else 'minutes'
