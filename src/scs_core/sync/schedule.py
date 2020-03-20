"""
Created on 29 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"scs-climate": {"interval": 60.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1},
"scs-particulates": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Schedule(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "schedule.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __sorted(cls, items):
        sorted_items = OrderedDict()

        for name in sorted(items.keys()):
            sorted_items[name] = items[name]

        return sorted_items


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return Schedule(OrderedDict())

        items = OrderedDict()

        for name, value_jdict in jdict.items():
            items[name] = ScheduleItem.construct_from_jdict(name, value_jdict)

        return Schedule(cls.__sorted(items))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items):
        """
        Constructor
        """
        self.__items = items                # dict of name: ScheduleItem


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        for item in self.__items.values():
            if not item.is_valid():
                return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def set(self, item):
        self.__items[item.name] = item

        self.__items = Schedule.__sorted(self.__items)


    def clear(self, name):
        if name not in self.__items:
            return False

        self.__items.pop(name)

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        if not self.is_valid():
            raise ValueError("Schedule.save: schedule is not valid.")

        super().save(host)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.__items


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def items(self):
        return self.__items.values()


    def contains(self, name):
        return name in self.__items


    def item(self, name):
        if name not in self.__items:
            return None

        return self.__items[name]


    def is_empty(self):
        return len(self.__items) == 0


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        items = '[' + ', '.join(str(item) for item in self.__items.values()) + ']'

        return "Schedule:{items:%s}" % items


# --------------------------------------------------------------------------------------------------------------------

class ScheduleItem(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, name, jdict):
        if not jdict:
            return None

        interval = jdict.get('interval')
        tally = jdict.get('tally')

        return ScheduleItem(name, interval, tally)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, interval, tally):
        """
        Constructor
        """
        self.__name = name
        self.__interval = round(float(interval), 1)                 # float     seconds between samples
        self.__tally = int(tally)                                   # int       number of samples per report


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__interval <= 0:
            return False

        if self.__tally < 1:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['interval'] = self.interval
        jdict['tally'] = self.tally

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def duration(self):
        return round(self.interval * self.tally, 1)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def interval(self):
        return self.__interval


    @property
    def tally(self):
        return self.__tally


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ScheduleItem:{name:%s, interval:%0.1f, tally:%d}" % (self.name, self.interval, self.tally)
