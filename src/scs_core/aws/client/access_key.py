"""
Created on 16 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import sys

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
    def get(cls):
        key = cls.from_environment()
        return key if key else cls.from_user()


    @classmethod
    def from_environment(cls):
        if cls.__ID_NAME not in os.environ or cls.__SECRET_NAME not in os.environ:
            return None

        id = os.environ[cls.__ID_NAME]
        secret = os.environ[cls.__SECRET_NAME]

        return cls(id, secret)


    @classmethod
    def from_user(cls):
        print("Enter AWS Access Key ID: ", end="", file=sys.stderr)
        id = input().strip()

        print("Enter AWS Secret Access Key: ", end="", file=sys.stderr)
        secret = input().strip()

        return cls(id, secret)


    @staticmethod
    def password_from_user():
        print("Enter password for AWS Access Key:", file=sys.stderr)
        return getpass().strip()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    @classmethod
    def construct_from_jdict(cls, jdict):
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
        self.__id = id                              # string
        self.__secret = secret                      # string


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
        return "AccessKey:{id:%s, secret:%s}" %  (self.id, self.secret)
