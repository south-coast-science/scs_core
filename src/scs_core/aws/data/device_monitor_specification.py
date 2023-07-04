"""
Created on 14 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"scs-opc-109": ["somebody@somewhere.com", "somebody@somewhere-else.com"], ...}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable, PersistentJSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitorSpecification(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if jdict is None:
            return None

        device_tag = jdict.get('device-tag')
        recipients = set(jdict.get('recipients'))
        is_suspended = jdict.get('suspended')

        return cls(device_tag, recipients, is_suspended)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_tag, recipients, is_suspended):
        """
        Constructor
        """
        super().__init__()

        self.__device_tag = device_tag                              # string
        self.__recipients = recipients                              # set of emails
        self.__is_suspended = bool(is_suspended)                    # bool


    def __len__(self):
        return len(self.__recipients)


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, email_address):
        self.__recipients.add(email_address)


    def discard(self, email_address):
        self.__recipients.discard(email_address)


    # ----------------------------------------------------------------------------------------------------------------

    def matches_tag(self, device_tag, exact):
        if device_tag is None:
            return True

        return (exact and device_tag == self.device_tag) or (not exact and device_tag in self.device_tag)


    def matches_email(self, email_address, exact):
        if email_address is None:
            return True

        for email in self.__recipients:
            if (exact and email_address == email) or (not exact and email_address in email):
                return True

        return False


    def contains_email(self, email_address):
        for email in self.__recipients:
            if email_address == email:
                return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['device-tag'] = self.device_tag
        jdict['recipients'] = self.recipients
        jdict['suspended'] = self.is_suspended

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device_tag(self):
        return self.__device_tag


    @property
    def recipients(self):
        return sorted(self.__recipients)


    @property
    def is_suspended(self):
        return self.__is_suspended


    @is_suspended.setter
    def is_suspended(self, is_suspended):
        self.__is_suspended = is_suspended


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceMonitorSpecification:{device_tag:%s, recipients:%s, is_suspended:%s}" %  \
            (self.device_tag, self.recipients, self.is_suspended)


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitorSpecificationList(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_monitor_specification_list.json"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if jdict is None:
            return None

        device_dict = {device_tag: DeviceMonitorSpecification.construct_from_jdict(specification_jdict)
                       for device_tag, specification_jdict in jdict.items()}

        return cls(device_dict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_dict):
        """
        Constructor
        """
        super().__init__()

        self.__device_dict = device_dict                            # dict of device-tag: DeviceMonitorSpecification


    def __len__(self):
        return len(self.__device_dict)


    def __contains__(self, item):
        return item in self.__device_dict


    # ----------------------------------------------------------------------------------------------------------------

    def set_suspended(self, device_tag, is_suspended):
        self.__device_dict[device_tag].is_suspended = is_suspended              # may raise KeyError

        return self.__device_dict[device_tag]


    def add(self, device_tag, email_address):
        if device_tag not in self.__device_dict:
            self.__device_dict[device_tag] = DeviceMonitorSpecification(device_tag, set(), False)

        self.__device_dict[device_tag].add(email_address)

        return self.__device_dict[device_tag]


    def discard(self, device_tag, email_address):
        device_dict = {}

        # all devices...
        if device_tag is None:
            for device_tag in self.__device_dict:
                self.__device_dict[device_tag].discard(email_address)
                device_dict[device_tag] = self.__device_dict[device_tag]

        # specific device...
        elif device_tag not in self.__device_dict:
            device_dict = {}

        else:
            self.__device_dict[device_tag].discard(email_address)
            device_dict = {device_tag: self.__device_dict[device_tag]}

        return DeviceMonitorSpecificationList(device_dict)


    def filter(self, email_address=None, device_tag=None, exact=False):
        device_dict = {}

        for specification in self.__device_dict():
            if not specification.matches_tag(device_tag, exact):
                continue

            if not specification.matches_email(email_address, exact):
                continue

            device_dict[specification.device_tag] = self.__device_dict[specification.device_tag]

        return DeviceMonitorSpecificationList(device_dict)


    def filter_devices(self, device_tags):
        device_dict = {key: self.__device_dict[key] for key in self.__device_dict.keys() & device_tags}

        return DeviceMonitorSpecificationList(device_dict)


    def subset(self, email_address):
        device_dict = {device_tag: specification for device_tag, specification in self.__device_dict.items()
                       if specification.contains_email(email_address)}

        return DeviceMonitorSpecificationList(device_dict)


    # ----------------------------------------------------------------------------------------------------------------

    def specification(self, device_tag):
        try:
            return self.__device_dict[device_tag]
        except KeyError:
            return None


    @property
    def device_dict(self):
        device_dict = {device_tag: specification for device_tag, specification in sorted(self.__device_dict.items())
                       if len(specification)}

        return device_dict


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.device_dict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceMonitorSpecificationList:{device_dict:%s}" %  Str.collection(self.device_dict)