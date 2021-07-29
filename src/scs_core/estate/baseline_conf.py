"""
Created on 25 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python

example JSON:
{"lab-timezone": "Europe/London", "start-hour": 23, "end-hour": 8, "aggregation-period": {"interval": 5, "units": "M"},
"gas-offsets": {"CO": 300, "NO": 10}}
"""

import pytz

from collections import OrderedDict
from datetime import datetime

from scs_core.data.json import PersistentJSONable
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.recurring_period import RecurringPeriod
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class BaselineConf(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------


    __FILENAME = "calibration_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        lab_timezone = jdict.get('lab-timezone')
        start_hour = jdict.get('start-hour')
        end_hour = jdict.get('end-hour')
        aggregation_period = RecurringPeriod.construct_from_jdict(jdict.get('aggregation-period'))
        gas_offsets = jdict.get('gas-offsets')

        return cls(lab_timezone, start_hour, end_hour, aggregation_period, gas_offsets)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lab_timezone, start_hour, end_hour, aggregation_period, gas_offsets):
        """
        Constructor
        """
        self.__lab_timezone = lab_timezone                      # string
        self.__start_hour = int(start_hour)                     # int
        self.__end_hour = int(end_hour)                         # int
        self.__aggregation_period = aggregation_period          # RecurringMinutes
        self.__gas_offsets = gas_offsets                        # dict of string: int


    # ----------------------------------------------------------------------------------------------------------------

    def start_datetime(self, origin: LocalizedDatetime):
        dt = origin.datetime
        tz = pytz.timezone(self.lab_timezone)

        start_dt = datetime(dt.year, month=dt.month, day=dt.day, hour=self.start_hour)
        start = LocalizedDatetime(tz.localize(start_dt))

        if self.start_hour > self.end_hour:
            start -= Timedelta(days=1)

        return start.utc()


    def end_datetime(self, origin: LocalizedDatetime):
        dt = origin.datetime
        tz = pytz.timezone(self.lab_timezone)

        end_dt = datetime(dt.year, month=dt.month, day=dt.day, hour=self.end_hour)
        end = LocalizedDatetime(tz.localize(end_dt))

        if end > origin:
            raise ValueError("the end datetime is in the future")

        return end.utc()


    def checkpoint(self):
        return self.aggregation_period.checkpoint()


    def add_gas(self, gas, offset):
        self.__gas_offsets[gas] = offset


    def remove_gas(self, gas):
        try:
            del self.__gas_offsets[gas]
        except KeyError:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def lab_timezone(self):
        return self.__lab_timezone


    @property
    def start_hour(self):
        return self.__start_hour


    @property
    def end_hour(self):
        return self.__end_hour


    @property
    def aggregation_period(self):
        return self.__aggregation_period


    @property
    def gas_offsets(self):
        return OrderedDict(sorted(self.__gas_offsets.items()))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['lab-timezone'] = self.lab_timezone
        jdict['start-hour'] = self.start_hour
        jdict['end-hour'] = self.end_hour
        jdict['aggregation-period'] = self.aggregation_period.as_json()
        jdict['gas-offsets'] = self.gas_offsets

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BaselineConf:{lab_timezone:%s, start_hour:%s, end_hour:%s, " \
               "aggregation_period:%s, gas_offsets:%s}" %  \
               (self.lab_timezone, self.start_hour, self.end_hour,
                self.aggregation_period, self.gas_offsets)
