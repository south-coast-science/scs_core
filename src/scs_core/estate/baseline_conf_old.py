"""
Created on 25 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python

example JSON:
{"timezone": "Europe/London", "start-hour": 17, "end-hour": 8, "aggregation-period": {"interval": 5, "units": "M"},
"gas-minimums": {"CO": 200, "CO2": 420, "H2S": 5, "NO": 10, "NO2": 10, "SO2": 5}}
"""

import pytz

from collections import OrderedDict
from datetime import datetime

from scs_core.data.json import MultiPersistentJSONable
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.recurring_period import RecurringPeriod
from scs_core.data.str import Str
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class BaselineConf(MultiPersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __SUPPORTED_GASES = ('CO', 'CO2', 'H2S', 'NO', 'NO2', 'Ox', 'SO2', 'VOC', 'VOCe')

    @classmethod
    def supported_gases(cls):
        return cls.__SUPPORTED_GASES


    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "baseline_conf.json"

    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))

        return cls.conf_dir(), filename


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, name=None, skeleton=False):
        if not jdict:
            return None

        timezone = jdict.get('timezone')
        start_hour = jdict.get('start-hour')
        end_hour = jdict.get('end-hour')
        aggregation_period = RecurringPeriod.construct_from_jdict(jdict.get('aggregation-period'), timezone=timezone)
        minimums = jdict.get('minimums')

        return cls(name, timezone, start_hour, end_hour, aggregation_period, minimums)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, timezone, start_hour, end_hour, aggregation_period, minimums):
        """
        Constructor
        """
        super().__init__(name)

        self.__timezone = timezone                              # string
        self.__start_hour = int(start_hour)                     # int
        self.__end_hour = int(end_hour)                         # int
        self.__aggregation_period = aggregation_period          # RecurringMinutes
        self.__minimums = minimums                              # dict of string: int


    # ----------------------------------------------------------------------------------------------------------------

    def duplicate(self, new_name):
        timezone = self.timezone
        start_hour = self.start_hour
        end_hour = self.end_hour
        aggregation_period = self.aggregation_period
        minimums = self.minimums

        return BaselineConf(new_name, timezone, start_hour, end_hour, aggregation_period, minimums)


    # ----------------------------------------------------------------------------------------------------------------

    def start_datetime(self, origin: LocalizedDatetime):
        dt = origin.datetime
        tz = pytz.timezone(self.timezone)

        start_dt = datetime(dt.year, month=dt.month, day=dt.day, hour=self.start_hour)
        start = LocalizedDatetime(tz.localize(start_dt))

        if self.start_hour > self.end_hour:
            start -= Timedelta(days=1)

        return start.utc()


    def end_datetime(self, origin: LocalizedDatetime):
        dt = origin.datetime
        tz = pytz.timezone(self.timezone)

        end_dt = datetime(dt.year, month=dt.month, day=dt.day, hour=self.end_hour)
        end = LocalizedDatetime(tz.localize(end_dt))

        return end.utc()


    def expected_data_points(self, start, end):
        points_per_hour = 60 / self.aggregation_period.interval
        period = end - start

        return int(points_per_hour * period.hours)


    def checkpoint(self):
        return self.aggregation_period.checkpoint()


    # ----------------------------------------------------------------------------------------------------------------

    def set_minimum(self, gas, value):
        self.__minimums[gas] = value


    def remove_minimum(self, gas):
        try:
            del self.__minimums[gas]
        except KeyError:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def timezone(self):
        return self.__timezone


    @property
    def start_hour(self):
        return self.__start_hour


    @property
    def end_hour(self):
        return self.__end_hour


    @property
    def aggregation_period(self):
        return self.__aggregation_period


    def minimum(self, gas):
        return self.__minimums[gas]


    @property
    def minimums(self):
        return OrderedDict(sorted(self.__minimums.items()))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['timezone'] = self.timezone
        jdict['start-hour'] = self.start_hour
        jdict['end-hour'] = self.end_hour
        jdict['aggregation-period'] = self.aggregation_period
        jdict['minimums'] = self.minimums

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        minimums = Str.collection(self.minimums)

        return "BaselineConf:{name:%s, timezone:%s, start_hour:%s, end_hour:%s, aggregation_period:%s, " \
               "minimums:%s}" %  \
               (self.name, self.timezone, self.start_hour, self.end_hour, self.aggregation_period,
                minimums)
