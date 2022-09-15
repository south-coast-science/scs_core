"""
Created on 09 Nov 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class EmailList(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_email_list"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        email_list = jdict.get('email_list')

        return cls(email_list)


    @staticmethod
    def __item_contains_address(addresses, email_address):
        if addresses is None:
            return False

        return email_address in addresses


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, email_list):
        """
        Constructor
        """
        super().__init__()

        self.__email_list = email_list


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, device_tag, email_address):
        if device_tag not in self.__email_list:
            return False

        if self.__email_list[device_tag] is None:
            self.__email_list[device_tag] = email_address
            return True

        if device_tag in self.__email_list[device_tag]:
            return True

        try:
            self.__email_list[device_tag].append(email_address)
            self.__email_list[device_tag].sort()

        except AttributeError:
            self.__email_list[device_tag] = sorted([email_address, self.__email_list[device_tag]])

        return True


    def remove(self, device_tag, email_address):
        # all devices...
        if device_tag is None:
            for listed_tag in self.__email_list:
                self.__remove_for_device(listed_tag, email_address)

            return True

        # specific device...
        if device_tag not in self.__email_list:
            return False

        self.__remove_for_device(device_tag, email_address)

        return True


    def __remove_for_device(self, device_tag, email_address):
        if self.__email_list[device_tag] is None:
            return

        try:
            try:
                self.__email_list[device_tag].remove(email_address)
            except ValueError:
                pass

        except AttributeError:
            if self.__email_list[device_tag] == email_address:
                self.__email_list[device_tag] = None


    # ----------------------------------------------------------------------------------------------------------------

    def subset(self, email_address):
        email_list = {device_tag: addresses for device_tag, addresses in self.__email_list.items()
                      if self.__item_contains_address(addresses, email_address)}

        return EmailList(email_list)


    def emails(self, device_tag):
        try:
            return self.__email_list[device_tag]
        except KeyError:
            return None


    @property
    def email_list(self):
        email_list = OrderedDict()
        for device_tag in sorted(self.__email_list):
            email_list[device_tag] = self.__email_list[device_tag]

        return email_list


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return {'email_list': self.email_list}


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "EmailList:{email_list:%s}" %  self.email_list
