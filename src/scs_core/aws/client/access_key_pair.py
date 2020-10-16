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

class AccessKeyPair(PersistentJSONable):
    """
    classdocs
    """

    ID_NAME = 'AWS_ACCESS_KEY_ID'
    SECRET_NAME = 'AWS_SECRET_ACCESS_KEY'

    __FILENAME =    "access_key_pair.json"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def from_user(cls):
        if cls.ID_NAME in os.environ:
            key_id = os.environ[cls.ID_NAME]
        else:
            print("Enter AWS Access Key ID: ", file=sys.stderr)
            key_id = input()

        if cls.SECRET_NAME in os.environ:
            secret_key = os.environ[cls.SECRET_NAME]
        else:
            print("Enter Secret AWS Access Key: ", file=sys.stderr)
            secret_key = getpass()

        return cls(key_id, secret_key)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls, host):
        return host.aws_dir(), cls.__FILENAME


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
        return "AccessKeyPair:{key_id:%s, secret_key:%s}" %  (self.key_id, self.secret_key)


