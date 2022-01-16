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

    ORG_ID = 'OrgID'
    LABEL = 'Label'
    LONG_NAME = 'LongName'
    URL = 'URL'
    OWNER = 'Owner'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_label(cls, label):
        try:
            if not (1 < len(label) < 256):
                return False

            return bool(re.fullmatch(r'[0-9A-Za-z\- &.()]+', label))

        except TypeError:
            return False


    @classmethod
    def is_valid_long_name(cls, long_name):
        try:
            return 1 < len(long_name) < 256

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

        org_id = jdict.get(cls.ORG_ID, 0)
        label = jdict.get(cls.LABEL)
        long_name = jdict.get(cls.LONG_NAME)
        url = jdict.get(cls.URL)
        owner = jdict.get(cls.OWNER)

        return cls(org_id, label, long_name, url, owner)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, org_id, label, long_name, url, owner):
        """
        Constructor
        """
        self.__org_id = int(org_id)                     # AUTO PK: int
        self.__label = label                            # UNIQUE: string
        self.__long_name = long_name                    # string
        self.__url = url                                # string
        self.__owner = owner                            # INDEX: string (email address)


    def __lt__(self, other):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):         # WARNING: does not test for name uniqueness
        return self.is_valid_label(self.label) and self.is_valid_long_name(self.long_name) and \
               self.is_valid_url(self.url) and self.is_valid_owner(self.owner)


    def as_json(self):
        jdict = OrderedDict()

        if self.org_id is not None:
            jdict[self.ORG_ID] = self.org_id

        jdict[self.LABEL] = self.label
        jdict[self.LONG_NAME] = self.long_name
        jdict[self.URL] = self.url
        jdict[self.OWNER] = self.owner

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def org_id(self):
        return self.__org_id


    @property
    def label(self):
        return self.__label


    @property
    def long_name(self):
        return self.__long_name


    @property
    def url(self):
        return self.__url


    @property
    def owner(self):
        return self.__owner


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{org_id:%s, label:%s, long_name:%s, url:%s, owner:%s}" % \
               (self.org_id, self.label, self.long_name, self.url, self.owner)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationPathRoot(JSONable):
    """
    classdocs
    """

    OPR_ID = 'OPRID'
    ORG_ID = 'OrgID'
    PATH = 'Path'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_path(cls, path):
        try:
            if len(path) > 255:
                return False

            return bool(re.fullmatch(r'[0-9A-Za-z\-]+/', path))

        except TypeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        opr_id = jdict.get(cls.OPR_ID, 0)
        org_id = jdict.get(cls.ORG_ID)
        path = jdict.get(cls.PATH)

        return cls(opr_id, org_id, path)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, opr_id, org_id, path):
        """
        Constructor
        """
        self.__opr_id = int(opr_id)                     # AUTO PK: int
        self.__org_id = int(org_id)                     # INDEX: int
        self.__path = path                              # UNIQUE: string


    def __lt__(self, other):
        return self.path < other.path


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):             # WARNING: does not test for path uniqueness
        if self.org_id is None:
            return False

        return self.is_valid_path(self.path)


    def as_json(self):
        jdict = OrderedDict()

        if self.opr_id is not None:
            jdict[self.OPR_ID] = self.opr_id

        jdict[self.ORG_ID] = self.org_id
        jdict[self.PATH] = self.path

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def opr_id(self):
        return self.__opr_id


    @property
    def org_id(self):
        return self.__org_id


    @property
    def path(self):
        return self.__path


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{opr_id:%s, org_id:%s, path:%s}" % \
               (self.opr_id, self.org_id, self.path)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationUser(JSONable):
    """
    classdocs
    """

    USERNAME = 'Username'
    ORG_ID = 'OrgID'
    IS_ORG_ADMIN = 'IsOrgAdmin'
    IS_DEVICE_ADMIN = 'IsDeviceAdmin'
    IS_VERIFIED = 'IsVerified'
    IS_SUSPENDED = 'IsSuspended'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        username = jdict.get(cls.USERNAME)
        org_id = jdict.get(cls.ORG_ID)
        is_org_admin = jdict.get(cls.IS_ORG_ADMIN)
        is_device_admin = jdict.get(cls.IS_DEVICE_ADMIN)
        is_verified = jdict.get(cls.IS_VERIFIED)
        is_suspended = jdict.get(cls.IS_SUSPENDED)

        return cls(username, org_id, is_org_admin, is_device_admin, is_verified, is_suspended)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, org_id, is_org_admin, is_device_admin, is_verified, is_suspended):
        """
        Constructor
        """
        self.__username = int(username)                 # PK: int
        self.__org_id = int(org_id)                     # PK: int
        self.__is_org_admin = bool(is_org_admin)        # INDEX: bool
        self.__is_device_admin = bool(is_device_admin)  # INDEX: bool
        self.__is_verified = bool(is_verified)          # INDEX: bool
        self.__is_suspended = bool(is_suspended)        # INDEX: bool


    def __lt__(self, other):                    # requires join with Cognito to do useful sort
        if self.username < other.username:
            return True

        if self.username > other.username:
            return False

        return self.org_id < other.org_id


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.username is None or self.org_id is None:
            return False

        return True


    def as_json(self):
        jdict = OrderedDict()

        jdict[self.USERNAME] = self.username
        jdict[self.ORG_ID] = self.org_id
        jdict[self.IS_ORG_ADMIN] = self.is_org_admin
        jdict[self.IS_DEVICE_ADMIN] = self.is_device_admin
        jdict[self.IS_VERIFIED] = self.is_verified
        jdict[self.IS_SUSPENDED] = self.is_suspended

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.__username


    @property
    def org_id(self):
        return self.__org_id


    @property
    def is_org_admin(self):
        return self.__is_org_admin


    @property
    def is_device_admin(self):
        return self.__is_device_admin


    @property
    def is_verified(self):
        return self.__is_verified


    @property
    def is_suspended(self):
        return self.__is_suspended


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{username:%s, org_id:%s, is_org_admin:%s, is_device_admin:%s, " \
                                         "is_verified:%s, is_suspended:%s}" % \
               (self.username, self.org_id, self.is_org_admin, self.is_device_admin,
                self.is_verified, self.is_suspended)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationUserPath(JSONable):
    """
    classdocs
    """

    USERNAME = 'Username'
    OPR_ID = 'OPRID'
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
        opr_id = jdict.get(cls.OPR_ID)
        extension = jdict.get(cls.EXTENSION)

        return cls(username, opr_id, extension)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, opr_id, extension):
        """
        Constructor
        """
        self.__username = int(username)                 # PK: int
        self.__opr_id = int(opr_id)                     # PK: int
        self.__extension = extension                    # PK: string


    def __lt__(self, other):
        if self.username < other.username:
            return True

        if self.username > other.username:
            return False

        if self.opr_id < other.opr_id:
            return True

        if self.opr_id > other.opr_id:
            return False

        return self.extension < other.extension


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.username is None or self.opr_id is None:
            return False

        return self.is_valid_extension(self.extension)


    def as_json(self):
        jdict = OrderedDict()

        jdict[self.USERNAME] = self.username
        jdict[self.OPR_ID] = self.opr_id
        jdict[self.EXTENSION] = self.extension

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.__username


    @property
    def opr_id(self):
        return self.__opr_id


    @property
    def extension(self):
        return self.__extension


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{username:%s, opr_id:%s, extension:%s}" %  \
               (self.username, self.opr_id, self.extension)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationDevice(JSONable):
    """
    classdocs
    """

    DEVICE_TAG = 'DeviceTag'
    ORG_ID = 'OrgID'
    START_DATETIME = 'StartDatetime'
    END_DATETIME = 'EndDatetime'
    DEPLOYMENT_LABEL = 'DeploymentLabel'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_tag(cls, device_tag):
        try:
            if len(device_tag) > 255:
                return False

            return bool(re.fullmatch(r'[a-z]+[0-9]*-[a-z]+[0-9]*-[0-9]+', device_tag))

        except TypeError:
            return False


    @classmethod
    def is_valid_deployment_label(cls, deployment_label):
        try:
            return 1 < len(deployment_label) < 256

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
        deployment_label = jdict.get(cls.DEPLOYMENT_LABEL)

        return cls(device_tag, org_id, start_datetime, end_datetime, deployment_label)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_tag, org_id, start_datetime, end_datetime, deployment_label):
        """
        Constructor
        """
        self.__device_tag = device_tag                  # PK: string
        self.__org_id = int(org_id)                     # PK: int
        self.__start_datetime = start_datetime          # NOT NONE: LocalizedDatetime
        self.__end_datetime = end_datetime              # LocalizedDatetime
        self.__deployment_label = deployment_label      # NOT NONE, UNIQUE(org_id, deployment_label): string


    def __lt__(self, other):
        if self.device_tag < other.device_tag:
            return True

        if self.device_tag > other.device_tag:
            return False

        if self.start_datetime < other.start_datetime:
            return True

        if self.start_datetime > other.start_datetime:
            return False

        return self.org_id < other.org_id


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.device_tag is None or self.org_id is None:
            return False

        return self.is_valid_tag(self.device_tag) and self.is_valid_deployment_label(self.deployment_label)


    def as_json(self):
        jdict = OrderedDict()

        jdict[self.DEVICE_TAG] = self.device_tag
        jdict[self.ORG_ID] = self.org_id
        jdict[self.START_DATETIME] = self.start_datetime.as_iso8601()
        jdict[self.END_DATETIME] = None if self.end_datetime is None else self.end_datetime.as_iso8601()
        jdict[self.DEPLOYMENT_LABEL] = self.deployment_label

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


    @property
    def deployment_label(self):
        return self.__deployment_label


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{device_tag:%s, org_id:%s, start_datetime:%s, end_datetime:%s, " \
                                         "deployment_label:%s}" % \
               (self.device_tag, self.org_id, self.start_datetime, self.end_datetime,
                self.deployment_label)
