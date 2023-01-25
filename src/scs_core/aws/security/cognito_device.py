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
    def construct_from_response(cls, res):
        if not res:
            return None

        tag = res.get('Username')
        created = LocalizedDatetime.construct_from_aws(str(res.get('UserCreateDate')))

        try:
            return cls(tag, None, created)
        except KeyError:
            return None


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, None, None) if skeleton else None

        tag = jdict.get('Username')
        shared_secret = jdict.get('password')
        created = LocalizedDatetime.construct_from_iso8601(jdict.get('UserCreateDate'))

        return cls(tag, shared_secret, created)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, shared_secret, created):
        """
        Constructor
        """
        super().__init__(tag, shared_secret)

        self._created = created                             # LocalisedDatetime


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
            jdict['Username'] = self.tag

        if self.shared_secret is not None:
            jdict['Password'] = self.shared_secret

        if self.created is not None:
            jdict['UserCreateDate'] = self.created.as_iso8601()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def created(self):
        return self._created


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoDeviceIdentity:{tag:%s, shared_secret:%s, created:%s}" % \
               (self.tag, self.shared_secret, self.created)
