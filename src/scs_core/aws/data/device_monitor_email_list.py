"""
Created on 14 Jun 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitorEmailList(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_monitor_email_list.json"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        device_dict = {device_tag: set(recipients) for device_tag, recipients in jdict.items()}

        return cls(device_dict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_dict):
        """
        Constructor
        """
        super().__init__()

        self.__device_dict = device_dict                            # dict of device-tag: set of emails


    def __len__(self):
        return len(self.__device_dict)


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, device_tag, email_address):
        if device_tag not in self.__device_dict:
            self.__device_dict[device_tag] = set()

        self.__device_dict[device_tag].add(email_address)


    def discard(self, device_tag, email_address):
        # all devices...
        if device_tag is None:
            for device_tag in self.__device_dict:
                self.__device_dict[device_tag].discard(email_address)
            return

        # specific device...
        if device_tag not in self.__device_dict:
            return

        self.__device_dict[device_tag].discard(email_address)


    def filter(self, email_address=None, device_tag=None, exact=False):
        device_dict = {}

        for key in self.__device_dict.keys():
            if device_tag is not None and not self.__tag_in_key(key, device_tag, exact):
                continue

            if email_address is not None and not self.__email_in_list(self.__device_dict[key], email_address, exact):
                continue

            device_dict[key] = self.__device_dict[key]

        return DeviceMonitorEmailList(device_dict)


    def filter_devices(self, device_tags):
        device_dict = {key: self.__device_dict[key] for key in self.__device_dict.keys() & device_tags}

        return DeviceMonitorEmailList(device_dict)


    @staticmethod
    def __tag_in_key(key, device_tag, exact):
        return (exact and device_tag == key) or (not exact and device_tag in key)


    @staticmethod
    def __email_in_list(email_list, email_address, exact):
        for email in email_list:
            if (exact and email_address == email) or (not exact and email_address in email):
                return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def subset(self, email_address):
        device_dict = {device_tag: recipients for device_tag, recipients in self.__device_dict.items()
                       if email_address in recipients}

        return DeviceMonitorEmailList(device_dict)


    def recipients(self, device_tag):
        try:
            return self.__device_dict[device_tag]
        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def device(self, device_tag):
        try:
            return self.__device_dict[device_tag]

        except KeyError:
            return None


    @property
    def device_dict(self):
        device_dict = OrderedDict()
        for device_tag in sorted(self.__device_dict):
            device_dict[device_tag] = sorted(self.__device_dict[device_tag])

        return device_dict


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.device_dict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceMonitorEmailList:{device_dict:%s}" %  Str.collection(self.device_dict)
