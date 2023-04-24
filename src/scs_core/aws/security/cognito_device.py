"""
Created on 5 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document (credentials):
{"username": "scs-opc-1", "password": "Ytzglk6oYpzJY0FB"}

example document (identity):
{"username": "scs-ph1-28", "created": "2023-04-04T09:08:55Z", "last-updated": "2023-04-04T09:08:56Z"}
"""

import re

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceCredentials(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_tag(cls, tag):
        if not isinstance(tag, str):
            return False

        return re.search(r'^\w+-\w+-\d+$', tag) is not None


    @staticmethod
    def is_valid_password(password):
        if not isinstance(password, str):
            return False

        return re.search(r'^\S{16}$', password) is not None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, password):
        """
        Constructor
        """
        self._tag = tag                                 # PK: string
        self.__password = password                      # string


    def __lt__(self, other):
        return self.tag < other.tag


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['username'] = self.tag
        jdict['password'] = self.password

        return jdict

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.tag


    @property
    def tag(self):
        return self._tag


    @property
    def password(self):
        return self.__password


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoDeviceCredentials:{tag:%s, password:%s}" % \
               (self.tag, self.password)


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceIdentity(CognitoDeviceCredentials):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_res(cls, res):
        if not res:
            return None

        tag = res.get('Username')
        password = res.get('password')

        created = round(LocalizedDatetime.construct_from_aws(str(res.get('UserCreateDate'))), 3).utc()
        last_updated = round(LocalizedDatetime.construct_from_aws(str(res.get('UserLastModifiedDate'))), 3).utc()

        return cls(tag, password, created, last_updated)


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, None, None, None) if skeleton else None

        tag = jdict.get('username')
        password = jdict.get('password')
        created = LocalizedDatetime.construct_from_iso8601(jdict.get('created'))
        last_updated = LocalizedDatetime.construct_from_iso8601(jdict.get('last-updated'))

        return cls(tag, password, created, last_updated)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, password, created, last_updated):
        """
        Constructor
        """
        super().__init__(tag, password)

        self._created = created                                 # LocalisedDatetime
        self._last_updated = last_updated                       # LocalizedDatetime


    def __eq__(self, other):
        try:
            return self.tag == other.tag

        except (TypeError, AttributeError):
            return False


    def __lt__(self, other):
        return self.tag < other.tag


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def index(self):
        return self.username


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.tag is not None:
            jdict['username'] = self.tag

        if self.password is not None:
            jdict['password'] = self.password

        if self.created is not None:
            jdict['created'] = self.created.as_iso8601()

        if self.last_updated is not None:
            jdict['last-updated'] = self.last_updated.as_iso8601()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def created(self):
        return self._created


    @property
    def last_updated(self):
        return self._last_updated


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoDeviceIdentity:{tag:%s, password:%s, created:%s, last_updated:%s}" % \
               (self.tag, self.password, self.created, self.last_updated)
