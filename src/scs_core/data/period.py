"""
Created on 10 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import pytz

from abc import abstractmethod, ABC

from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class Period(ABC):
    """
    classdocs
    """

    @classmethod
    @abstractmethod
    def type(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, timezone: pytz.timezone):
        self.__timezone = timezone                          # pytz.timezone


    @abstractmethod
    def __lt__(self, other):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def is_valid(self):
        pass


    @abstractmethod
    def has_expiring_dst(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def checkpoint(self):
        pass


    @abstractmethod
    def cron(self, minutes_offset):
        pass


    @abstractmethod
    def aws_cron(self, minutes_offset):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def start_datetime(self, point: LocalizedDatetime):
        pass


    @abstractmethod
    def end_datetime(self, origin: LocalizedDatetime):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def timezone(self):
        return self.__timezone


    @timezone.setter
    def timezone(self, timezone):
        self.__timezone = timezone
