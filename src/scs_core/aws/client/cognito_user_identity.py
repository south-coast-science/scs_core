"""
Created on 22 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/2520893/how-to-flush-the-input-stream-in-python

example document:
{"email-address": "bruno.beloff@southcoastscience.com", "password": "hello"}
"""

import json
import sys
import termios

from collections import OrderedDict
from getpass import getpass

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserIdentity(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "cognito_user_identity.json"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def from_stdin(cls):
        line = sys.stdin.readline()
        jdict = json.loads(line)

        return cls.construct_from_jdict(jdict)


    @classmethod
    def from_user(cls):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)               # flush stdin
        except termios.error:
            pass

        print("Enter email address: ", end="", file=sys.stderr)
        email_address = input().strip()

        print("Enter password: ", end="", file=sys.stderr)
        password = input().strip()

        return cls(email_address, password)


    @staticmethod
    def password_from_user():
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)               # flush stdin
        except termios.error:
            pass

        return getpass().strip()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, None) if skeleton else None

        email_address = jdict.get('email-address')
        password = jdict.get('password')

        return cls(email_address, password)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, email_address, password):
        """
        Constructor
        """
        super().__init__()

        self.__email_address = email_address                    # string
        self.__password = password                              # string


    # ----------------------------------------------------------------------------------------------------------------

    def ok(self):
        if not self.email_address or not self.password:
            return False

        if not Datum.is_email_address(self.email_address):
            return False

        return True


    def get_token(self):
        # TODO: implement get_token()
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['email-address'] = self.email_address
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
        return "CognitoUserIdentity:{email_address:%s, password:%s}" %  (self.email_address, self.password)
