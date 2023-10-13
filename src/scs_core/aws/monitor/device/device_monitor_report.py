"""
Created on 17 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example (DeviceReport):
{"device-tag": "scs-be2-3",
"availability": {"is-ok": true, "since": "2023-06-19T16:57:25Z"},
"data": {"south-coast-science-dev/development/device/alpha-bb-eng-000003/status":
{"is-ok": true, "since": "2023-06-19T16:57:25Z"},
"south-coast-science-dev/development/loc/1/climate": {"is-ok": true, "since": "2023-06-19T16:57:25Z"},
"south-coast-science-dev/development/loc/1/gases": {"is-ok": true, "since": "2023-06-19T16:57:25Z"},
"south-coast-science-dev/development/loc/1/particulates": {"is-ok": true, "since": "2023-06-19T16:57:25Z"}},
"power": {"is-ok": null, "since": "2023-06-19T16:57:25Z"},
"uptime": {"period": "00-03:34:00"}}

document example (DeviceMonitorMessage):
{"change": {"device-tag": "scs-be2-3", "cause": "TOPIC_INACTIVE", "topic": "test/topic"},
"status": {"device-tag": "scs-be2-3", "availability": {"is-ok": false, "since": "2023-10-11T14:45:35Z"},
"data": {"south-coast-science-dev/development/device/alpha-bb-eng-000003/status":
{"is-ok": true, "since": "2023-07-06T13:00:32Z"}, "south-coast-science-dev/development/loc/1/climate":
{"is-ok": true, "since": "2023-10-02T13:30:37Z"}, "south-coast-science-dev/development/loc/1/gases":
{"is-ok": true, "since": "2023-10-02T12:45:36Z"}, "south-coast-science-dev/development/loc/1/particulates":
{"is-ok": true, "since": "2023-10-10T11:45:35Z"}}, "power": {"is-ok": true, "since": "2023-07-04T15:42:10Z"},
"uptime": {"period": "00-00:53:00"}}}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable, JSONify, PersistentJSONable
from scs_core.data.str import Str
from scs_core.data.timedelta import Timedelta

from scs_core.email.email import Email


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

        self.__is_ok = bool(is_ok)                                  # bool
        self.__since = since                                        # LocalizedDatetime or None


    def __eq__(self, other):
        try:
            return self.is_ok == other.is_ok

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def delta(self, prev_report):
        if prev_report is None:
            return None

        if self.is_ok == prev_report.is_ok:
            return None

        return self.is_ok


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['is-ok'] = self.is_ok
        jdict['since'] = None if self.since is None else self.since.utc()

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

        period = Timedelta.construct_from_jdict(jdict.get('period'))

        return cls(period)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, period: Timedelta):
        """
        Constructor
        """
        super().__init__()

        self.__period = period                                      # Timedelta


    def __eq__(self, other):
        try:
            return self.period == other.period

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def delta(self, prev_report):
        if prev_report is None:
            return None

        if prev_report.period is None:
            return None

        if self.period < prev_report.period:
            return False

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['period'] = self.period

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def period(self):
        return self.__period


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceUptime:{period:%s}" %  self.period


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

        self.__topic_dict = topic_dict                                  # dict of string: DeviceStatus


    def __len__(self):
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

    def status(self, topic):
        try:
            return self.__topic_dict[topic]

        except KeyError:
            return None


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

    def matches(self, device_tag, exact):
        if device_tag is None:
            return True

        return (exact and device_tag == self.device_tag) or (not exact and device_tag in self.device_tag)


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


    @property
    def data(self):
        return self.__data


    @property
    def power(self):
        return self.__power


    @property
    def uptime(self):
        return self.__uptime


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
        if jdict is None:
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


    def device(self, device_tag):
        try:
            return self.__device_dict[device_tag]
        except KeyError:
            return None


    def filter(self, device_tag=None, exact=False):
        device_dict = {key: report for key, report in self.__device_dict.items() if report.matches(device_tag, exact)}

        return DeviceMonitorReport(device_dict)


    def filter_devices(self, device_tags):
        device_dict = {key: self.__device_dict[key] for key in self.__device_dict.keys() & device_tags}

        return DeviceMonitorReport(device_dict)


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


# --------------------------------------------------------------------------------------------------------------------

class DeviceStatusChange(JSONable):
    """
    classdocs
    """

    CAUSE_ILLEGAL_VALUES = "ILLEGAL_VALUES"
    CAUSE_LEGAL_VALUES = "LEGAL_VALUES"
    CAUSE_POWER_LOST = "POWER_LOST"
    CAUSE_POWER_RESTORED = "POWER_RESTORED"
    CAUSE_OFFLINE = "OFFLINE"
    CAUSE_ONLINE = "ONLINE"
    CAUSE_TOPIC_INACTIVE = "TOPIC_INACTIVE"
    CAUSE_TOPIC_ACTIVE = "TOPIC_ACTIVE"
    CAUSE_UPTIME = "UPTIME"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device_tag = jdict.get('device-tag')
        cause = jdict.get('cause')
        topic = jdict.get('topic')

        return cls(device_tag, cause, topic)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_tag, cause, topic=None):
        """
        Constructor
        """
        self.__device_tag = device_tag                              # string
        self.__cause = cause                                        # string
        self.__topic = topic                                        # string or None


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['device-tag'] = self.device_tag
        jdict['cause'] = self.cause

        if self.topic is not None:
            jdict['topic'] = self.topic

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device_tag(self):
        return self.__device_tag


    @property
    def cause(self):
        return self.__cause


    @property
    def topic(self):
        return self.__topic


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceStatusChange:{device_tag:%s, cause:%s, topic:%s}" %  (self.device_tag, self.cause, self.topic)


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitorMessage(Email, JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        change = DeviceStatusChange.construct_from_jdict(jdict.get('change'))
        status = DeviceReport.construct_from_jdict(jdict.get('status'))

        return cls(change, status)


    @classmethod
    def construct(cls, status: DeviceReport, cause, topic=None):
        change = DeviceStatusChange(status.device_tag, cause, topic=topic)

        return cls(change, status)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, change: DeviceStatusChange, status: DeviceReport):
        """
        Constructor
        """
        self.__change = change                                      # DeviceStatusChange
        self.__status = status                                      # DeviceReport


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def subject(self):
        return JSONify.dumps(self.change)


    @property
    def body(self):
        return JSONify.dumps(self)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['change'] = self.change
        jdict['status'] = self.status

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def change(self):
        return self.__change


    @property
    def status(self):
        return self.__status


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceMonitorMessage:{change:%s, status:%s}" %   (self.change, self.status)
