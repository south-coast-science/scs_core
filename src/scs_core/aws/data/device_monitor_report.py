"""
Created on 17 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example (DeviceReport):
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable, PersistentJSONable
from scs_core.data.str import Str
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class DeviceStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        is_ok = jdict.get('is-ok')
        since = LocalizedDatetime.construct_from_jdict(jdict.get('since'))

        return cls(is_ok, since)


    @classmethod
    def construct_for_state(cls, is_ok: bool):
        return cls(is_ok, LocalizedDatetime.now())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, is_ok: bool, since):
        """
        Constructor
        """
        super().__init__()

        self.__is_ok = is_ok                                        # bool
        self.__since = since                                        # LocalizedDatetime or None


    def __eq__(self, other):
        try:
            return self.is_ok == other.is_ok

        except AttributeError:
            return False


    def __bool__(self):
        return self.is_ok


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['is-ok'] = self.is_ok
        jdict['since'] = self.since

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_ok(self):
        return self.__is_ok


    @property
    def since(self):
        return self.__since


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceStatus:{is_ok:%s, since:%s}" %  (self.is_ok, self.since)


# --------------------------------------------------------------------------------------------------------------------

class DeviceUptime(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        uptime = Timedelta.construct_from_jdict(jdict.get('since'))

        return cls(uptime)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uptime: Timedelta):
        """
        Constructor
        """
        super().__init__()

        self.__uptime = uptime                                      # Timedelta


    def __eq__(self, other):
        try:
            return self.uptime == other.uptime

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['uptime'] = self.uptime

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def uptime(self):
        return self.__uptime


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceUptime:{uptime:%s}" %  self.uptime


# --------------------------------------------------------------------------------------------------------------------

class TopicStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        topic_dict = {topic: DeviceStatus.construct_from_jdict(status_jdict)
                      for topic, status_jdict in jdict.items()}

        return cls(topic_dict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic_dict):
        """
        Constructor
        """
        super().__init__()

        self.__topic_dict = topic_dict                                      # dict of string: DeviceStatus


    def __len(self):
        return len(self.__topic_dict.items())


    # ----------------------------------------------------------------------------------------------------------------

    def is_ok(self):
        for status in self.__topic_dict.values():
            if not status.is_ok():
                return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.topic_dict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic_dict(self):
        return dict(sorted(self.__topic_dict.items()))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicStatus:{topic_dict:%s}" %  Str.collection(self.topic_dict)


# --------------------------------------------------------------------------------------------------------------------

class DeviceReport(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device_tag = jdict.get('device-tag')

        availability = DeviceStatus.construct_from_jdict(jdict.get('availability'))
        data = TopicStatus.construct_from_jdict(jdict.get('data'))
        power = DeviceStatus.construct_from_jdict(jdict.get('power'))
        uptime = DeviceUptime.construct_from_jdict(jdict.get('uptime'))

        return cls(device_tag, availability, data, power, uptime)


    @classmethod
    def construct_for_device(cls, device_tag):
        return cls(device_tag, None, None, None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_tag, availability, data, power, uptime):
        """
        Constructor
        """
        super().__init__()

        self.__device_tag = device_tag                              # string

        self.__availability = availability                          # DeviceStatus or None
        self.__data = data                                          # TopicStatus or None
        self.__power = power                                        # DeviceStatus or None
        self.__uptime = uptime                                      # DeviceUptime or None


    def __eq__(self, other):
        try:
            return self.device_tag == other.device_tag and \
                self.availability == other.availability and self.data == other.data and \
                self.power == other.power and self.uptime == other.uptime

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['device-tag'] = self.device_tag

        jdict['availability'] = self.availability
        jdict['data'] = self.data
        jdict['power'] = self.power
        jdict['uptime'] = self.uptime

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device_tag(self):
        return self.__device_tag


    @property
    def availability(self):
        return self.__availability


    @availability.setter
    def availability(self, is_ok: bool):
        self.__availability = DeviceStatus.construct_for_state(is_ok)


    @property
    def data(self):
        return self.__data


    @data.setter
    def data(self, is_ok: bool):
        self.__data = DeviceStatus.construct_for_state(is_ok)


    @property
    def power(self):
        return self.__power


    @power.setter
    def power(self, is_ok: bool):
        self.__power = DeviceStatus.construct_for_state(is_ok)


    @property
    def uptime(self):
        return self.__uptime


    @uptime.setter
    def uptime(self, is_ok: bool):
        self.__uptime = DeviceStatus.construct_for_state(is_ok)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceReport:{device_tag:%s, availability:%s, data:%s, power:%s, uptime:%s}" %  \
            (self.device_tag, self.availability, self.data, self.power, self.uptime)


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitorReport(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_monitor_report.json"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        device_dict = {device_tag: DeviceReport.construct_from_jdict(report_jdict)
                       for device_tag, report_jdict in jdict.items()}

        return cls(device_dict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_dict):
        """
        Constructor
        """
        super().__init__()

        self.__device_dict = device_dict                            # dict of device-tag: DeviceReport


    def __contains__(self, device_tag):
        return device_tag in self.__device_dict


    def __len__(self):
        return len(self.__device_dict)


    # ----------------------------------------------------------------------------------------------------------------

    def insert(self, report: DeviceReport):
        self.__device_dict[report.device_tag] = report


    def report(self, device_tag):
        try:
            return self.__device_dict[device_tag]
        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.device_dict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device_dict(self):
        return dict(sorted(self.__device_dict.items()))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceMonitorReport:{device_dict:%s}" %  Str.collection(self.device_dict)
