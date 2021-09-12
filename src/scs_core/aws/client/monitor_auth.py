"""
Created on 20 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"email": "bruno.beloff@southcoastscience.com", "password": "XXX"}
"""

import sys
import termios

from collections import OrderedDict
from getpass import getpass

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class MonitorAuth(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "monitor_auth.json"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def from_user(cls):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)           # flush stdin
        except termios.error:
            pass

        print("Email address: ", end="", file=sys.stderr)
        email_address = input().strip()

        print("Password: ", end="", file=sys.stderr)
        password = getpass().strip()

        return cls(email_address, password)


    @staticmethod
    def password_from_user():
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)           # flush stdin
        except termios.error:
            pass

        return getpass().strip()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        email_address = jdict.get('email')
        password = jdict.get('password')

        return cls(email_address, password)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, email_address, password):
        """
        Constructor
        """
        super().__init__()

        self.__email_address = email_address                # String
        self.__password = password                          # String


    # ----------------------------------------------------------------------------------------------------------------

    def has_valid_email_address(self):
        return Datum.is_email_address(self.email_address)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['email'] = self.email_address
        jdict['password'] = self.password

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def email_address(self):
        return self.__email_address


    @property
    def password(self):
        return self.__password


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MonitorAuth:{email_address:%s, password:%s}" % (self.email_address, self.password)
