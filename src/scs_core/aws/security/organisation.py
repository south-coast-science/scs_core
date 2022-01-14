"""
Created on 26 Oct 2021

@author: Jade Page (jade.page@southcoastscience.com)

The foundation data classes for the security system
"""

import re

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Organisation(JSONable):
    """
    classdocs
    """

    ORG_ID = 'OrganisationID'
    NAME = 'Name'
    URL = 'URL'
    OWNER = 'Owner'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_name(cls, name):
        try:
            if len(name) > 255:
                return False

            return bool(re.fullmatch(r'([0-9A-Za-z\- .()]+)', name))

        except TypeError:
            return False


    @classmethod
    def is_valid_url(cls, url):
        try:
            if len(url) > 255:
                return False

            return Datum.is_url(url)

        except TypeError:
            return False


    @classmethod
    def is_valid_owner(cls, owner):
        try:
            if len(owner) > 255:
                return False

            return Datum.is_email_address(owner)

        except TypeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        org_id = jdict.get(cls.ORG_ID)
        name = jdict.get(cls.NAME)
        url = jdict.get(cls.URL)
        owner = jdict.get(cls.OWNER)

        return cls(org_id, name, url, owner)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, org_id, name, url, owner):
        """
        Constructor
        """
        self.__org_id = int(org_id)                     # PK: int
        self.__name = name                              # UNIQUE: string
        self.__url = url                                # string
        self.__owner = owner                            # INDEX: string (email address)


    def __lt__(self, other):
        return self.name < other.name


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.is_valid_name(self.name) and self.is_valid_url(self.url) and self.is_valid_owner(self.owner)


    def as_json(self):
        jdict = OrderedDict()

        jdict[self.ORG_ID] = self.org_id
        jdict[self.NAME] = self.name
        jdict[self.URL] = self.url
        jdict[self.OWNER] = self.owner

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def org_id(self):
        return self.__org_id


    @property
    def name(self):
        return self.__name


    @property
    def url(self):
        return self.__url


    @property
    def owner(self):
        return self.__owner


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Organisation:{org_id:%s, name:%s, url:%s, owner:%s}" % \
               (self.org_id, self.name, self.url, self.owner)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationPathRoot(JSONable):
    """
    classdocs
    """

    PATH_ID = 'PathID'
    ORG_ID = 'OrganisationID'
    PATH = 'Path'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_path(cls, path):
        try:
            if len(path) > 255:
                return False

            return bool(re.fullmatch(r'([0-9A-Za-z\-]+/)', path))

        except TypeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        path_id = jdict.get(cls.PATH_ID)
        org_id = jdict.get(cls.ORG_ID)
        path = jdict.get(cls.PATH)

        return cls(path_id, org_id, path)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path_id, org_id, path):
        """
        Constructor
        """
        self.__path_id = int(path_id)                   # PK: int
        self.__org_id = int(org_id)                     # INDEX: int
        self.__path = path                              # UNIQUE: string


    def __lt__(self, other):
        return self.path < other.path


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.is_valid_path(self.path)


    def as_json(self):
        jdict = OrderedDict()

        jdict[self.PATH_ID] = self.path_id
        jdict[self.ORG_ID] = self.org_id
        jdict[self.PATH] = self.path

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path_id(self):
        return self.__path_id


    @property
    def org_id(self):
        return self.__org_id


    @property
    def path(self):
        return self.__path


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OrganisationPathRoot:{path_id:%s, org_id:%s, path:%s}" % \
               (self.path_id, self.org_id, self.path)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationAdmin(JSONable):
    """
    classdocs
    """

    USERNAME = 'Username'
    ORG_ID = 'OrganisationID'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        username = jdict.get(cls.USERNAME)
        org_id = jdict.get(cls.ORG_ID)

        return cls(username, org_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, org_id):
        """
        Constructor
        """
        self.__username = int(username)                 # PK: int
        self.__org_id = int(org_id)                     # PK: int


    def __lt__(self, other):
        if self.username < other.username:
            return True

        if self.username > other.username:
            return False

        return self.org_id < other.org_id


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict[self.USERNAME] = self.username
        jdict[self.ORG_ID] = self.org_id

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.__username


    @property
    def org_id(self):
        return self.__org_id


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OrganisationAdmin:{username:%s, org_id:%s}" % \
               (self.username, self.org_id)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationUser(JSONable):
    """
    classdocs
    """

    USERNAME = 'Username'
    ORG_ID = 'OrganisationID'
    VERIFIED = 'Verified'
    SUSPENDED = 'Suspended'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        username = jdict.get(cls.USERNAME)
        org_id = jdict.get(cls.ORG_ID)
        verified = jdict.get(cls.VERIFIED)
        suspended = jdict.get(cls.SUSPENDED)

        return cls(username, org_id, verified, suspended)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, org_id, verified, suspended):
        """
        Constructor
        """
        self.__username = int(username)                 # PK: int
        self.__org_id = int(org_id)                     # PK: int
        self.__verified = bool(verified)                # INDEX: bool
        self.__suspended = bool(suspended)              # INDEX: bool


    def __lt__(self, other):
        if self.username < other.username:
            return True

        if self.username > other.username:
            return False

        return self.org_id < other.org_id


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict[self.USERNAME] = self.username
        jdict[self.ORG_ID] = self.org_id
        jdict[self.VERIFIED] = self.verified
        jdict[self.SUSPENDED] = self.suspended

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.__username


    @property
    def org_id(self):
        return self.__org_id


    @property
    def verified(self):
        return self.__verified


    @property
    def suspended(self):
        return self.__suspended


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OrganisationUser:{username:%s, org_id:%s, verified:%s, suspended:%s}" % \
               (self.username, self.org_id, self.verified, self.suspended)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationUserPath(JSONable):
    """
    classdocs
    """

    USERNAME = 'Username'
    PATH_ID = 'PathID'
    EXTENSION = 'Extension'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_extension(cls, extension):
        try:
            if len(extension) > 255:
                return False

            return bool(re.fullmatch(r'([0-9A-Za-z\-]+/)+', extension))

        except TypeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        username = jdict.get(cls.USERNAME)
        path_id = jdict.get(cls.PATH_ID)
        extension = jdict.get(cls.EXTENSION)

        return cls(username, path_id, extension)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, path_id, extension):
        """
        Constructor
        """
        self.__username = int(username)                 # PK: int
        self.__path_id = int(path_id)                   # PK: int
        self.__extension = extension                    # NOT NONE: string


    def __lt__(self, other):
        if self.username < other.username:
            return True

        if self.username > other.username:
            return False

        if self.path_id < other.path_id:
            return True

        if self.path_id > other.path_id:
            return False

        return self.extension < other.extension


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.is_valid_extension(self.extension)


    def as_json(self):
        jdict = OrderedDict()

        jdict[self.USERNAME] = self.username
        jdict[self.PATH_ID] = self.path_id
        jdict[self.EXTENSION] = self.extension

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.__username


    @property
    def path_id(self):
        return self.__path_id


    @property
    def extension(self):
        return self.__extension


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OrganisationUserPath:{username:%s, path_id:%s, extension:%s}" % \
               (self.username, self.path_id, self.extension)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationDevice(JSONable):
    """
    classdocs
    """

    DEVICE_TAG = 'DeviceTag'
    ORG_ID = 'OrganisationID'
    START_DATETIME = 'StartDatetime'
    END_DATETIME = 'EndDatetime'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_tag(cls, device_tag):
        try:
            if len(device_tag) > 255:
                return False

            return bool(re.fullmatch(r'[a-z]+[0-9]*-[a-z]+[0-9]*-[0-9]+', device_tag))

        except TypeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device_tag = jdict.get(cls.DEVICE_TAG)
        org_id = jdict.get(cls.ORG_ID)
        start_datetime = LocalizedDatetime.construct_from_iso8601(jdict.get(cls.START_DATETIME))
        end_datetime = LocalizedDatetime.construct_from_iso8601(jdict.get(cls.END_DATETIME))

        return cls(device_tag, org_id, start_datetime, end_datetime)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_tag, org_id, start_datetime, end_datetime):
        """
        Constructor
        """
        self.__device_tag = device_tag                  # PK: string
        self.__org_id = int(org_id)                     # PK: int
        self.__start_datetime = start_datetime          # NOT NONE: LocalizedDatetime
        self.__end_datetime = end_datetime              # LocalizedDatetime


    def __lt__(self, other):
        if self.device_tag < other.device_tag:
            return True

        if self.device_tag > other.device_tag:
            return False

        return self.org_id < other.org_id


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.is_valid_tag(self.device_tag)


    def as_json(self):
        jdict = OrderedDict()

        jdict[self.DEVICE_TAG] = self.device_tag
        jdict[self.ORG_ID] = self.org_id
        jdict[self.START_DATETIME] = self.start_datetime.as_iso8601()
        jdict[self.END_DATETIME] = None if self.end_datetime is None else self.end_datetime.as_iso8601()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device_tag(self):
        return self.__device_tag


    @property
    def org_id(self):
        return self.__org_id


    @property
    def start_datetime(self):
        return self.__start_datetime


    @property
    def end_datetime(self):
        return self.__end_datetime


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OrganisationDevice:{device_tag:%s, org_id:%s, start_datetime:%s, end_datetime:%s}" % \
               (self.device_tag, self.org_id, self.start_datetime, self.end_datetime)
