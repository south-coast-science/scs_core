"""
Created on 29 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"scs-climate": {"interval": 60.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1},
"scs-particulates": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable, PersistentJSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class Schedule(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "schedule.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __sorted(cls, items):
        sorted_items = OrderedDict()

        for name in sorted(items.keys()):
            sorted_items[name] = items[name]

        return sorted_items


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(OrderedDict()) if skeleton else None

        items = OrderedDict()

        for name, value_jdict in jdict.items():
            items[name] = ScheduleItem.construct_from_jdict(name, value_jdict)

        return cls(cls.__sorted(items))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items):
        """
        Constructor
        """
        super().__init__()

        self.__items = items                # dict of name: ScheduleItem


    def __eq__(self, other):
        try:
            if list(self.names()) != list(other.names()):
                return False

            for name in self.names():
                if self.item(name) != other.item(name):
                    return False

            return True

        except (TypeError, AttributeError):
            return False


    def __contains__(self, item):
        return item in self.__items


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

    def save(self, host, encryption_key=None):
        if not self.is_valid():
            raise ValueError("Schedule.save: schedule is not valid.")

        super().save(host, encryption_key=encryption_key)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.__items


    # ----------------------------------------------------------------------------------------------------------------

    def names(self):
        return self.__items.keys()


    @property
    def items(self):
        return self.__items.values()


    def item(self, name):
        if name not in self.__items:
            return None

        return self.__items[name]


    def is_empty(self):
        return len(self.__items) == 0


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Schedule:{items:%s}" % Str.collection(self.__items)


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


    def __eq__(self, other):
        try:
            return self.name == other.name and self.interval == other.interval and \
                   self.tally == other.tally

        except (TypeError, AttributeError):
            return False


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
