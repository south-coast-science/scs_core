"""
Created on 26 Oct 2021

@author: Jade Page (jade.page@southcoastscience.com)

The foundation data classes for the security system

example Organisation:
{"OrgID": 1, "Label": "SCS", "LongName": "South Coast Science", "URL": "https://www.southcoastscience.com",
"Owner": "bruno.beloff@southcoastscience.com"}

example OrganisationPathRoot:
{"OPRID": 11, "OrgID": 1, "PathRoot": "ricardo/"}

example OrganisationUser:
{"Username": 111, "OrgID": 1, "IsOrgAdmin": true, "IsDeviceAdmin": true, "IsSuspended": false}

example OrganisationUserPath:
{"Username": 111, "OPRID": 11, "PathExtension": "heathrow/"}

example OrganisationDevice:
{"DeviceTag": "scs-bgx-401", "OrgID": 1, "DevicePath": "south-coast-science-demo/brighton/loc/1/",
"EnvironmentPath": "south-coast-science-demo/brighton/device/praxis-000401/",
"StartDatetime": "2022-01-17T10:40:04Z", "EndDatetime": null,
"DeploymentLabel": "Preston Circus"}
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

    def is_valid(self):         # WARNING: does not test for label uniqueness
        return self.is_valid_label(self.label) and self.is_valid_long_name(self.long_name) and \
               self.is_valid_url(self.url) and self.is_valid_owner(self.owner)


    def as_json(self):
        jdict = OrderedDict()

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

    @org_id.setter
    def org_id(self, org_id):
        self.__org_id = org_id


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
        name = self.__class__.__name__

        return name + ":{org_id:%s, label:%s, long_name:%s, url:%s, owner:%s}" % \
            (self.org_id, self.label, self.long_name, self.url, self.owner)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationPathRoot(JSONable):
    """
    classdocs
    """

    OPR_ID = 'OPRID'
    ORG_ID = 'OrgID'
    PATH_ROOT = 'PathRoot'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_path_root(cls, path_root):
        try:
            if len(path_root) > 255:
                return False

            return bool(re.fullmatch(r'[0-9A-Za-z\-]+/', path_root))

        except TypeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        opr_id = jdict.get(cls.OPR_ID, 0)
        org_id = jdict.get(cls.ORG_ID)
        path_root = jdict.get(cls.PATH_ROOT)

        return cls(opr_id, org_id, path_root)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, opr_id, org_id, path_root):
        """
        Constructor
        """
        self.__opr_id = int(opr_id)                     # AUTO PK: int
        self.__org_id = int(org_id)                     # INDEX: int
        self.__path_root = path_root                    # UNIQUE: string


    def __lt__(self, other):
        return self.path_root < other.path_root


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):             # WARNING: does not test for path root uniqueness
        if self.org_id is None:
            return False

        return self.is_valid_path_root(self.path_root)


    def as_json(self):
        jdict = OrderedDict()

        jdict[self.OPR_ID] = self.opr_id
        jdict[self.ORG_ID] = self.org_id
        jdict[self.PATH_ROOT] = self.path_root

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def opr_id(self):
        return self.__opr_id


    @opr_id.setter
    def opr_id(self, opr_id):
        self.__opr_id = opr_id



    @property
    def org_id(self):
        return self.__org_id


    @property
    def path_root(self):
        return self.__path_root


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        name = self.__class__.__name__

        return name + ":{opr_id:%s, org_id:%s, path_root:%s}" % \
            (self.opr_id, self.org_id, self.path_root)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationUser(JSONable):
    """
    classdocs
    """

    USERNAME = 'Username'
    ORG_ID = 'OrgID'
    IS_ORG_ADMIN = 'IsOrgAdmin'
    IS_DEVICE_ADMIN = 'IsDeviceAdmin'
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
        is_suspended = jdict.get(cls.IS_SUSPENDED)

        return cls(username, org_id, is_org_admin, is_device_admin, is_suspended)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, org_id, is_org_admin, is_device_admin, is_suspended):
        """
        Constructor
        """
        self.__username = username                      # PK: int
        self.__org_id = org_id                          # PK: int
        self.__is_org_admin = bool(is_org_admin)        # INDEX: bool
        self.__is_device_admin = bool(is_device_admin)  # INDEX: bool
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
    def is_suspended(self):
        return self.__is_suspended


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        name = self.__class__.__name__

        return name + ":{username:%s, org_id:%s, is_org_admin:%s, is_device_admin:%s, is_suspended:%s}" % \
            (self.username, self.org_id, self.is_org_admin, self.is_device_admin, self.is_suspended)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationUserPath(JSONable):
    """
    classdocs
    """

    USERNAME = 'Username'
    OPR_ID = 'OPRID'
    PATH_EXTENSION = 'PathExtension'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_path_extension(cls, path_extension):
        try:
            if len(path_extension) > 255:
                return False

            return bool(re.fullmatch(r'([0-9A-Za-z\-]+/)+', path_extension))

        except TypeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        username = jdict.get(cls.USERNAME)
        opr_id = jdict.get(cls.OPR_ID)
        path_extension = jdict.get(cls.PATH_EXTENSION)

        return cls(username, opr_id, path_extension)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, opr_id, path_extension):
        """
        Constructor
        """
        self.__username = int(username)                 # PK: int
        self.__opr_id = int(opr_id)                     # PK: int
        self.__path_extension = path_extension          # PK: string


    def __lt__(self, other):
        if self.username < other.username:
            return True

        if self.username > other.username:
            return False

        if self.opr_id < other.opr_id:
            return True

        if self.opr_id > other.opr_id:
            return False

        return self.path_extension < other.path_extension


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.username is None or self.opr_id is None:
            return False

        return self.is_valid_path_extension(self.path_extension)


    def as_json(self):
        jdict = OrderedDict()

        jdict[self.USERNAME] = self.username
        jdict[self.OPR_ID] = self.opr_id
        jdict[self.PATH_EXTENSION] = self.path_extension

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.__username


    @property
    def opr_id(self):
        return self.__opr_id


    @property
    def path_extension(self):
        return self.__path_extension


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        name = self.__class__.__name__

        return name + ":{username:%s, opr_id:%s, path_extension:%s}" %  \
            (self.username, self.opr_id, self.path_extension)


# --------------------------------------------------------------------------------------------------------------------

class OrganisationDevice(JSONable):
    """
    classdocs
    """

    DEVICE_TAG = 'DeviceTag'
    ORG_ID = 'OrgID'
    DEVICE_PATH = 'DevicePath'
    LOCATION_PATH = 'LocationPath'
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


    @classmethod
    def is_valid_path(cls, path):
        try:
            if len(path) > 255:
                return False

            return bool(re.fullmatch(r'([0-9A-Za-z\-]+/)+', path))

        except TypeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device_tag = jdict.get(cls.DEVICE_TAG)
        org_id = jdict.get(cls.ORG_ID)
        device_path = jdict.get(cls.DEVICE_PATH)
        location_path = jdict.get(cls.LOCATION_PATH)

        start_datetime = LocalizedDatetime.construct_from_iso8601(jdict.get(cls.START_DATETIME))
        end_datetime = LocalizedDatetime.construct_from_iso8601(jdict.get(cls.END_DATETIME))
        deployment_label = jdict.get(cls.DEPLOYMENT_LABEL)

        return cls(device_tag, org_id, device_path, location_path, start_datetime, end_datetime, deployment_label)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_tag, org_id, device_path, location_path, start_datetime, end_datetime,
                 deployment_label):
        """
        Constructor
        """
        self.__device_tag = device_tag                  # PK: string
        self.__org_id = int(org_id)                     # PK: int
        self.__device_path = device_path                # PK: string
        self.__location_path = location_path            # PK: string

        self.__start_datetime = start_datetime          # NOT NONE: LocalizedDatetime
        self.__end_datetime = end_datetime              # LocalizedDatetime
        self.__deployment_label = deployment_label      # INDEX: string


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

        return self.is_valid_tag(self.device_tag) and self.is_valid_deployment_label(self.deployment_label) and \
            self.is_valid_path(self.device_path) and self.is_valid_path(self.location_path)


    def as_json(self):
        jdict = OrderedDict()

        jdict[self.DEVICE_TAG] = self.device_tag
        jdict[self.ORG_ID] = self.org_id
        jdict[self.DEVICE_PATH] = self.device_path
        jdict[self.LOCATION_PATH] = self.location_path

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
    def device_path(self):
        return self.__device_path


    @property
    def location_path(self):
        return self.__location_path


    @property
    def start_datetime(self):
        return self.__start_datetime


    @property
    def end_datetime(self):
        return self.__end_datetime


    @end_datetime.setter
    def end_datetime(self, end_datetime):
        self.__end_datetime = end_datetime

    @start_datetime.setter
    def start_datetime(self, start_datetime):
        self.__start_datetime = start_datetime


    @property
    def deployment_label(self):
        return self.__deployment_label


    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        name = self.__class__.__name__

        return name + ":{device_tag:%s, org_id:%s, device_path:%s, location_path:%s, " \
                      "start_datetime:%s, end_datetime:%s, deployment_label:%s}" % \
            (self.device_tag, self.org_id, self.device_path, self.location_path,
             self.start_datetime, self.end_datetime, self.deployment_label)
