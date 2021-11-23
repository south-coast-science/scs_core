"""
Created on 22 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/2520893/how-to-flush-the-input-stream-in-python

example document:
{"email": "bruno.beloff@southcoastscience.com", "password": "hello"}
"""

import json
import sys
import termios

from collections import OrderedDict
from getpass import getpass

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserCredentials(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "cognito_user_credentials.json"

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
        email = input().strip()

        print("Enter password: ", end="", file=sys.stderr)
        password = input().strip()

        return cls(email, password)


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

        email = jdict.get('email')
        password = jdict.get('password')

        return cls(email, password)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, email, password):
        """
        Constructor
        """
        super().__init__()

        self.__email = email                            # string
        self.__password = password                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def ok(self):
        if not self.email or not self.password:
            return False

        if not Datum.is_email_address(self.email):
            return False

        return True


    def get_token(self):
        # TODO: implement get_token()
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['email'] = self.email
        jdict['password'] = self.password

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def email(self):
        return self.__email


    @property
    def password(self):
        return self.__password


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserCredentials:{email:%s, password:%s}" %  (self.email, self.password)
