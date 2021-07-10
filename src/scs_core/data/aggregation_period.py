"""
Created on 7 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"interval": 1, "units": "D"}
"""

import pytz

from abc import abstractmethod
from collections import OrderedDict
from datetime import datetime

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class AggregationPeriod(JSONable):
    """
    classdocs
    """
    _UTC = pytz.timezone('Etc/UTC')

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        interval = jdict.get('interval')
        units = jdict.get('units')

        return cls.construct(interval, units)


    @classmethod
    def construct(cls, interval, units):
        if units == 'D':
            return DayAggregationPeriod(interval)

        if units == 'H':
            return HoursAggregationPeriod(interval)

        if units == 'M':
            return MinutesAggregationPeriod(interval)

        raise ValueError(units)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interval):
        """
        Constructor
        """
        self.__interval = int(interval)                     # int


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def is_valid(self):
        pass


    @abstractmethod
    def checkpoint(self):
        pass


    @abstractmethod
    def cron(self, minutes_offset):
        pass


    @abstractmethod
    def timedelta(self):
        pass


    @abstractmethod
    def end_datetime(self, origin: LocalizedDatetime):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['interval'] = self.interval
        jdict['units'] = self.units

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def interval(self):
        return self.__interval


    @property
    @abstractmethod
    def units(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{interval:%s}" %  self.interval


# --------------------------------------------------------------------------------------------------------------------

class DayAggregationPeriod(AggregationPeriod):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interval):
        """
        Constructor
        """
        super().__init__(interval)


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.interval == 1


    def checkpoint(self):
        return '00:00:00'


    def cron(self, minutes_offset):
        return '%d 0 * * *' % minutes_offset


    def timedelta(self):
        return Timedelta(weeks=0, days=self.interval)


    def end_datetime(self, origin: LocalizedDatetime):
        dt = origin.utc().datetime

        return LocalizedDatetime(datetime(dt.year, month=dt.month, day=dt.day, tzinfo=self._UTC))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def units(self):
        return 'D'


# --------------------------------------------------------------------------------------------------------------------

class HoursAggregationPeriod(AggregationPeriod):
    """
    classdocs
    """

    __DIVISORS = (1, 2, 3, 4, 6, 8, 12)

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interval):
        """
        Constructor
        """
        super().__init__(interval)


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.interval in self.__DIVISORS


    def checkpoint(self):
        return '/%d:00:00' % self.interval


    def cron(self, minutes_offset):
        return '%d */%d * * *' % (minutes_offset, self.interval)


    def timedelta(self):
        return Timedelta(weeks=0, days=0, hours=self.interval)


    def end_datetime(self, origin: LocalizedDatetime):
        dt = origin.utc().datetime
        hour = (dt.hour // self.interval) * self.interval

        return LocalizedDatetime(datetime(dt.year, month=dt.month, day=dt.day, hour=hour, tzinfo=self._UTC))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def units(self):
        return 'H'


# --------------------------------------------------------------------------------------------------------------------

class MinutesAggregationPeriod(AggregationPeriod):
    """
    classdocs
    """

    __DIVISORS = (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30)

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interval):
        """
        Constructor
        """
        super().__init__(interval)


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.interval in self.__DIVISORS


    def checkpoint(self):
        return '**:/%d:00' % self.interval


    def cron(self, minutes_offset):
        minutes = [str(minute + minutes_offset) for minute in range(0, 60, self.interval)]

        return '%s * * * *' % ','.join(minutes)


    def timedelta(self):
        return Timedelta(weeks=0, days=0, hours=0, minutes=self.interval)


    def end_datetime(self, origin: LocalizedDatetime):
        dt = origin.utc().datetime
        minute = (dt.minute // self.interval) * self.interval

        return LocalizedDatetime(datetime(dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=minute,
                                          tzinfo=self._UTC))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def units(self):
        return 'M'
