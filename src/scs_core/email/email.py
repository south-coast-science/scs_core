"""
Created on 12 Oct 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod
from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Email(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def subject(self):
        pass


    @property
    @abstractmethod
    def body(self):
        pass


# --------------------------------------------------------------------------------------------------------------------

class EmailRecipient(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if jdict is None:
            return None

        email_address = jdict.get('email')
        json_message = jdict.get('json-message')

        return cls(email_address, json_message)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, email_address, json_message):
        """
        Constructor
        """
        super().__init__()

        self.__email_address = email_address                        # string
        self.__json_message = bool(json_message)                    # bool


    def __lt__(self, other):
        return self.__email_address.lower() < other.__email_address.lower()


    def __eq__(self, other):
        try:
            return self.email_address == other.email_address
        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['email'] = self.email_address
        jdict['json-message'] = self.json_message

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def email_address(self):
        return self.__email_address


    @property
    def json_message(self):
        return self.__json_message


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "EmailRecipient:{email_address:%s, json_message:%s}" %  (self.email_address, self.json_message)
