"""
Created on 5 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document (credentials):
{"username": "scs-opc-1", "password": "Ytzglk6oYpzJY0FB"}

example document (identity):
{"username": "scs-ap1-343", "created": "2022-04-07T13:37:56Z"}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceCredentials(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def is_valid_password(password):
        if not isinstance(password, str):
            return False

        return len(password) > 15


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, shared_secret):
        """
        Constructor
        """
        self.__tag = tag                                # string
        self.__shared_secret = shared_secret            # string


    def __lt__(self, other):
        return self.tag < other.tag


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['Username'] = self.tag
        jdict['Password'] = self.shared_secret

        return jdict

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def shared_secret(self):
        return self.__shared_secret


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoDeviceCredentials:{tag:%s, shared_secret:%s}" % \
               (self.tag, self.shared_secret)


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
        created = round(LocalizedDatetime.construct_from_aws(str(res.get('UserCreateDate'))), 3)
        last_updated = round(LocalizedDatetime.construct_from_aws(str(res.get('UserLastModifiedDate'))), 3)

        try:
            return cls(tag, None, created, last_updated)
        except KeyError:
            return None


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, None, None, None) if skeleton else None

        tag = jdict.get('username')
        shared_secret = jdict.get('password')
        created = LocalizedDatetime.construct_from_iso8601(jdict.get('created'))
        last_updated = LocalizedDatetime.construct_from_iso8601(jdict.get('last-updated'))

        return cls(tag, shared_secret, created, last_updated)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, shared_secret, created, last_updated):
        """
        Constructor
        """
        super().__init__(tag, shared_secret)

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

    def as_json(self):
        jdict = OrderedDict()

        if self.tag is not None:
            jdict['username'] = self.tag

        if self.shared_secret is not None:
            jdict['password'] = self.shared_secret

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
        return self.__class__.__name__ + ":{tag:%s, shared_secret:%s, created:%s, last_updated:%s}" % \
               (self.tag, self.shared_secret, self.created, self.last_updated)
