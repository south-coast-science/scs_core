"""
Created on 24 Oct 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A tool to specify time intervals that are aligned to the clock - a bit like crontab.

Checkpoints are specified in the form HH:MM:SS, in a format similar to that for crontab:

** - all values
NN - exactly matching NN
/NN - repeated every NN

For example, **:/5:30 is used to indicate 30 seconds past the minute, every 5 minutes, during every hour.
"""

from datetime import datetime, timedelta

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class CheckpointGenerator(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, specification):
        pieces = specification.split(':')

        if len(pieces) != 3:
            raise ValueError(specification)

        try:
            hour = CheckpointField.construct(pieces[0], 24)
            minute = CheckpointField.construct(pieces[1], 60)
            second = CheckpointField.construct(pieces[2], 60)

        except ValueError:
            raise ValueError(specification)

        return cls(hour, minute, second)


    @classmethod
    def is_valid(cls, specification):
        try:
            cls.construct(specification)
            return True

        except (AttributeError, ValueError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, hour, minute, second):
        """
        Constructor
        """
        self.__hour = hour                    # CheckpointField
        self.__minute = minute                # CheckpointField
        self.__second = second                # CheckpointField


    # ----------------------------------------------------------------------------------------------------------------

    def min_interval(self):
        interval = self.__second.interval(1)
        if interval is not None:
            return interval

        interval = self.__minute.interval(60)
        if interval is not None:
            return interval

        interval = self.__hour.interval(3600)
        if interval is not None:
            return interval

        return 86400            # 24 hours


    def min_timedelta(self):
        return Timedelta.construct(timedelta(seconds=self.min_interval()))


    # ----------------------------------------------------------------------------------------------------------------

    def enclosing_localised_datetime(self, localised_datetime):
        if self.aligns(localised_datetime):
            return localised_datetime

        return self.next_localised_datetime(localised_datetime)


    # if localised_datetime is on a boundary then next_localised_datetime(..) returns a future checkpoint

    def next_localised_datetime(self, localised_datetime):
        # parse...
        date_time = localised_datetime.datetime
        tzinfo = localised_datetime.tzinfo

        date = date_time.date()
        time = date_time.time()

        # compute...
        day_increment, next_hour, next_minute, next_second = self.next(time.hour, time.minute, time.second)

        # construct...
        checkpoint = datetime(date.year, month=date.month, day=date.day,
                              hour=next_hour, minute=next_minute, second=next_second, tzinfo=tzinfo)

        if day_increment:
            checkpoint += timedelta(days=1)

        return LocalizedDatetime(checkpoint)


    # if localised_datetime is on a boundary then prev_localised_datetime(..) returns the same checkpoint

    def prev_localised_datetime(self, localised_datetime):
        # parse...
        date_time = localised_datetime.datetime
        tzinfo = localised_datetime.tzinfo

        date = date_time.date()
        time = date_time.time()

        # compute...
        day_decrement, prev_hour, prev_minute, prev_second = self.prev(time.hour, time.minute, time.second)

        # construct...
        checkpoint = datetime(date.year, month=date.month, day=date.day,
                              hour=prev_hour, minute=prev_minute, second=prev_second, tzinfo=tzinfo)

        if day_decrement:
            checkpoint -= timedelta(days=1)

        return LocalizedDatetime(checkpoint)


    # ----------------------------------------------------------------------------------------------------------------

    def aligns(self, localised_datetime):
        date_time = localised_datetime.datetime
        t = date_time.time()

        return self.__hour.aligns(t.hour) and self.__minute.aligns(t.minute) and self.__second.aligns(t.second) \
            and t.microsecond == 0


    # if hour, minute, second are on a boundary then next(..) returns a future checkpoint

    def next(self, hour, minute, second):
        # seconds...
        next_second = self.__second.next(second)

        # minutes...
        if next_second > second:
            minute -= 1                        # current minute should be tested

        next_minute = self.__minute.next(minute)

        # hours...
        if next_minute > minute:
            hour -= 1                          # current hour should be tested

        next_hour = self.__hour.next(hour)

        # dateline...
        day_increment = self.is_24h() or (next_hour < hour)

        return day_increment, next_hour, next_minute, next_second


    # if hour, minute, second are on a boundary then prev(..) returns the same checkpoint

    def prev(self, hour, minute, second):
        # seconds...
        prev_second = self.__second.prev(second)

        # minutes...
        prev_minute = self.__minute.prev(minute)

        # hours...
        prev_hour = self.__hour.prev(hour)

        # dateline...
        day_decrement = prev_hour > hour

        return day_decrement, prev_hour, prev_minute, prev_second


    # ----------------------------------------------------------------------------------------------------------------

    def is_24h(self):
        return len(self.__hour) == 1 and len(self.__minute) == 1 and len(self.__second) == 1


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CheckpointGenerator:{hour:%s, minute:%s, second:%s}" % (self.__hour, self.__minute, self.__second)


# --------------------------------------------------------------------------------------------------------------------

class CheckpointField(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, specification, size):
        if not 0 < len(specification) < 4:
            raise ValueError(specification)

        # all ticks...
        if specification == "**":
            return CheckpointField([tick for tick in range(0, size, 1)])

        # stepped ticks...
        if specification[0] == '/':
            step = int(specification[1:])

            if not 0 < step < size:
                raise ValueError(specification)

            return CheckpointField([tick for tick in range(0, size, step)])

        # one tick...
        tick = int(specification)

        if not 0 <= tick < size:
            raise ValueError(specification)

        return CheckpointField([tick])


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ticks):
        """
        Constructor
        """
        self.__ticks = ticks                    # array of int


    def __len__(self):
        return len(self.__ticks)


    # ----------------------------------------------------------------------------------------------------------------

    def interval(self, period):
        if len(self) < 2:
            return None

        return (self.__ticks[1] - self.__ticks[0]) * period


    # ----------------------------------------------------------------------------------------------------------------

    def aligns(self, value):
        return bool(value in self.__ticks)


    def next(self, value):
        for tick in self.__ticks:
            if tick > value:
                return tick

        return self.__ticks[0]


    def prev(self, value):
        for tick in reversed(self.__ticks):
            if tick <= value:
                return tick

        return self.__ticks[-1]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CheckpointField:{ticks:%s}" % self.__ticks
