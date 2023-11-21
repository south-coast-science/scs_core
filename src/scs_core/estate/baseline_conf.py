"""
Created on 25 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python

example JSON:
{"sample-period": {"type": "diurnal", "start": "23:00:00", "end": "08:00:00", "timezone": "Europe/London"},
"aggregation-period": {"type": "recurring", "interval": 5, "units": "M", "timezone": "Europe/London"},
"minimums": {"CO": 300, "CO2": 420, "H2S": 5, "NO": 10, "NO2": 10, "Ox": 50, "SO2": 5, "VOC": 250}}
"""

import os

from collections import OrderedDict

from scs_core.data.json import MultiPersistentJSONable
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.diurnal_period import DiurnalPeriod
from scs_core.data.recurring_period import RecurringPeriod
from scs_core.data.str import Str


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

        return os.path.join(cls.conf_dir(), 'baseline_conf'), filename


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, name=None, skeleton=False):
        if not jdict:
            return cls(None, None, None, {}) if skeleton else None

        sample_period = DiurnalPeriod.construct_from_jdict(jdict.get('sample-period'))
        aggregation_period = RecurringPeriod.construct_from_jdict(jdict.get('aggregation-period'))
        minimums = jdict.get('minimums')

        return cls(name, sample_period, aggregation_period, minimums)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, sample_period, aggregation_period, minimums):
        """
        Constructor
        """
        super().__init__(name)

        self.__sample_period = sample_period                    # DiurnalPeriod
        self.__aggregation_period = aggregation_period          # RecurringPeriod
        self.__minimums = minimums                              # dict of string: int


    # ----------------------------------------------------------------------------------------------------------------

    def duplicate(self, new_name):
        sample_period = self.sample_period
        aggregation_period = self.aggregation_period
        minimums = self.minimums

        return BaselineConf(new_name, sample_period, aggregation_period, minimums)


    # ----------------------------------------------------------------------------------------------------------------

    def start_datetime(self, origin: LocalizedDatetime):
        return self.sample_period.start_datetime(origin)


    def end_datetime(self, origin: LocalizedDatetime):
        return self.sample_period.end_datetime(origin)


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
    def sample_period(self):
        return self.__sample_period


    @property
    def aggregation_period(self):
        return self.__aggregation_period

    @property
    def timezone(self):
        return None if self.sample_period is None else self.sample_period.timezone


    @property
    def gases(self):
        return set(sorted(self.__minimums.keys()))


    def minimum(self, gas):
        return self.__minimums[gas]


    @property
    def minimums(self):
        return OrderedDict(sorted(self.__minimums.items()))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['sample-period'] = self.sample_period
        jdict['aggregation-period'] = self.aggregation_period
        jdict['minimums'] = self.minimums

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BaselineConf:{name:%s, sample_period:%s, aggregation_period:%s, minimums:%s}" %  \
               (self.name, self.sample_period, self.aggregation_period, Str.collection(self.minimums))
