"""
Created on 24 Oct 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A tool to specify time intervals that are aligned to the clock - a little bit like crontab.

Example specifications:
**:/15:00   -   every 15 minutes
00:/15:00   -   every 15 minutes between midnight and 1am
**:15:00    -   every hour, at 15 minutes past the hour
"""

from datetime import datetime
from datetime import timedelta

from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class Checkpoint(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, specification):
        pieces = specification.split(':')

        if len(pieces) != 3:
            raise ValueError(specification)

        hour = CheckpointUnit.construct(pieces[0], 24)
        minute = CheckpointUnit.construct(pieces[1], 60)
        second = CheckpointUnit.construct(pieces[2], 60)

        return Checkpoint(hour, minute, second)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, hour, minute, second):
        """
        Constructor
        """
        self.__hour = hour                    # CheckpointUnit
        self.__minute = minute                # CheckpointUnit
        self.__second = second                # CheckpointUnit


    # ----------------------------------------------------------------------------------------------------------------

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
        day_increment = (next_hour < hour)

        return day_increment, next_hour, next_minute, next_second


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Checkpoint:{hour:%s, minute:%s, second:%s}" % \
               (self.__hour, self.__minute, self.__second)


# --------------------------------------------------------------------------------------------------------------------

class CheckpointUnit(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, specification, size):
        if not 2 <= len(specification) <= 3:
            raise ValueError(specification)

        # all ticks...
        if specification == "**":
            return CheckpointUnit([tick for tick in range(0, size, 1)])

        # stepped ticks...
        if specification[0] == '/':
            step = int(specification[1:])

            if step >= size:
                raise ValueError(specification)

            return CheckpointUnit([tick for tick in range(0, size, step)])

        # one tick...
        tick = int(specification)

        if tick >= size:
            raise ValueError(specification)

        return CheckpointUnit([tick])


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ticks):
        """
        Constructor
        """
        self.__ticks = ticks                    # array of int


    # ----------------------------------------------------------------------------------------------------------------

    def next(self, value):
        for tick in self.__ticks:
            if tick > value:
                return tick

        return self.__ticks[0]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CheckpointUnit:{ticks:%s}" % self.__ticks
