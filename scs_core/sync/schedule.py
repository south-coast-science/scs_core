"""
Created on 29 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
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
    def filename(cls, host):
        return host.conf_dir() + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return Schedule(OrderedDict())

        items = OrderedDict()

        for name, value_jdict in jdict.items():
            items[name] = ScheduleItem.construct_from_jdict(name, value_jdict)

        return Schedule(items)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items):
        """
        Constructor
        """
        self.__items = items


    # ----------------------------------------------------------------------------------------------------------------

    def set(self, item):
        self.__items[item.name] = item


    def clear(self, name):
        if name not in self.__items:
            return False

        self.__items.pop(name)

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.__items


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def items(self):
        return self.__items.values()


    def item(self, name):
        if name not in self.__items:
            return None

        return self.__items[name]


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
        self.__interval = Datum.float(interval, 1)          # time between samples
        self.__tally = Datum.int(tally)                     # number of samples per report


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['interval'] = self.interval
        jdict['tally'] = self.tally

        return jdict


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
        return "ScheduleItem:{name:%s, interval:%0.1f, tally:%d}" % \
               (self.name, self.interval, self.tally)
