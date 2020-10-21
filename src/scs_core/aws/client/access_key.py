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
    def from_environment(cls):
        if cls.__ID_NAME not in os.environ or cls.__SECRET_NAME not in os.environ:
            return None

        key_id = os.environ[cls.__ID_NAME]
        secret_key = os.environ[cls.__SECRET_NAME]

        return cls(key_id, secret_key)


    @classmethod
    def from_user(cls):
        print("Enter AWS Access Key ID:", file=sys.stderr)
        key_id = input()

        print("Enter AWS Secret Access Key:", file=sys.stderr)
        secret_key = input()

        return cls(key_id, secret_key)


    @staticmethod
    def password_from_user():
        print("Enter password for AWS Access Key:", file=sys.stderr)
        return getpass()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        key_id = jdict.get('key-id')
        secret_key = jdict.get('secret-key')

        return cls(key_id, secret_key)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, key_id, secret_key):
        """
        Constructor
        """
        self.__key_id = key_id                              # string
        self.__secret_key = secret_key                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['key-id'] = self.key_id
        jdict['secret-key'] = self.secret_key

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def key_id(self):
        return self.__key_id


    @property
    def secret_key(self):
        return self.__secret_key


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AccessKey:{key_id:%s, secret_key:%s}" %  (self.key_id, self.secret_key)
