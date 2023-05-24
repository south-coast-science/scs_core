"""
Created on 16 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/2520893/how-to-flush-the-input-stream-in-python

document example:
{"key-id": "ABC", "secret-key": "123"}
"""

import json
import os
import sys
import termios

from collections import OrderedDict
from getpass import getpass

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class AccessKey(PersistentJSONable):
    """
    classdocs
    """

    __ID_NAME = 'AWS_ACCESS_KEY_ID'
    __SECRET_NAME = 'AWS_SECRET_ACCESS_KEY'

    __FILENAME = "access_key.json"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def from_stdin(cls):
        line = sys.stdin.readline()
        jdict = json.loads(line)

        return cls.construct_from_jdict(jdict)


    @classmethod
    def from_environment(cls):
        if cls.__ID_NAME not in os.environ or cls.__SECRET_NAME not in os.environ:
            return None

        id = os.environ[cls.__ID_NAME]
        secret = os.environ[cls.__SECRET_NAME]

        return cls(id, secret)


    @classmethod
    def from_user(cls):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)           # flush stdin
        except termios.error:
            pass

        print("Enter AWS Access Key ID: ", end="", file=sys.stderr)
        id = input().strip()

        print("Enter AWS Secret Access Key: ", end="", file=sys.stderr)
        secret = input().strip()

        return cls(id, secret)


    @staticmethod
    def password_from_user():
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)  # flush stdin
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
            return None

        id = jdict.get('key-id')
        secret = jdict.get('secret-key')

        return cls(id, secret)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, secret):
        """
        Constructor
        """
        super().__init__()

        self.__id = id  # string
        self.__secret = secret  # string


    # ----------------------------------------------------------------------------------------------------------------

    def ok(self):
        return self.id and self.secret


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['key-id'] = self.id
        jdict['secret-key'] = self.secret

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def secret(self):
        return self.__secret


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AccessKey:{id:%s, secret:%s}" % (self.id, self.secret)
