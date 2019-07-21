"""
Created on 24 Oct 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A tool to specify time intervals that are aligned to the clock - a little bit like crontab.

Checkpoints are specified in the form HH:MM:SS, in a format similar to that for crontab:

** - all values
NN - exactly matching NN
/NN - every match of NN

For example, **:/5:30 is used to indicate 30 seconds past the minute, every 5 minutes, during every hour.
"""

from datetime import datetime
from datetime import timedelta

from scs_core.data.localized_datetime import LocalizedDatetime


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

        hour = CheckpointField.construct(pieces[0], 24)
        minute = CheckpointField.construct(pieces[1], 60)
        second = CheckpointField.construct(pieces[2], 60)

        return CheckpointGenerator(hour, minute, second)


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

    def enclosing_localised_datetime(self, localised_datetime):
        if self.aligns(localised_datetime):
            return localised_datetime

        return self.next_localised_datetime(localised_datetime)


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


    # ----------------------------------------------------------------------------------------------------------------

    def aligns(self, localised_datetime):
        date_time = localised_datetime.datetime
        t = date_time.time()

        return self.__hour.aligns(t.hour) and self.__minute.aligns(t.minute) and self.__second.aligns(t.second) \
            and t.microsecond == 0


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
        if not 1 < len(specification) < 4:
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

    def aligns(self, value):
        return bool(value in self.__ticks)


    def next(self, value):
        for tick in self.__ticks:
            if tick > value:
                return tick

        return self.__ticks[0]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CheckpointField:{ticks:%s}" % self.__ticks
