"""
Created on 5 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document (credentials):
{"username": "scs-opc-1", "password": "########"}

example document (identity):
{"username": "scs-bgx-401", "password": "########", "invoice": "INV-000123",
"created": "2023-06-23T10:32:52+01:00", "last-updated": "2023-06-23T10:32:52+01:00"}
"""

import re

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable

from scs_core.sys.logging import Logging
from scs_core.sys.shared_secret import SharedSecret
from scs_core.sys.system_id import SystemID


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceCredentials(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load_credentials_for_device(cls, host, strict=True):
        logger = Logging.getLogger()

        # SystemID...
        system_id = SystemID.load(host)

        if not system_id:
            if strict:
                logger.error("SystemID not available.")
                exit(1)
            else:
                return None

        # SharedSecret...
        shared_secret = SharedSecret.load(host)

        if not shared_secret:
            if strict:
                logger.error("SharedSecret not available.")
                exit(1)
            else:
                return None

        return cls(system_id.message_tag(), shared_secret.key)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_tag(cls, tag):
        try:
            if len(tag) > 255:
                return False

            return bool(re.fullmatch(r'[a-z]+\d*-[a-z]+\d*-\d+', tag))

        except TypeError:
            return False



    @classmethod
    def is_valid_password(cls, password):
        if not isinstance(password, str):
            return False

        return re.search(r'^\S{16,255}$', password) is not None


    @classmethod
    def multiple_tags(cls, prototype_tag, number):
        if not cls.is_valid_tag(prototype_tag):
            raise ValueError(prototype_tag)

        pieces = prototype_tag.split('-')

        vendor_id = pieces[0]
        model_id = pieces[1]
        system_serial = int(pieces[2])

        for system_serial_number in range(system_serial, system_serial + number):
            yield '-'.join((vendor_id, model_id, str(system_serial_number)))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, password):
        """
        Constructor
        """
        self._tag = tag                                         # PK: string
        self.__password = password                              # string


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

    @classmethod
    def is_valid_invoice_number(cls, invoice_number):
        try:
            match = re.match(r'INV-\d{4,}', invoice_number)
            return match is not None

        except TypeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_res(cls, res):
        if not res:
            return None

        tag = res.get('Username')
        password = res.get('password')

        invoice_number = res.get('invoice')

        created = round(LocalizedDatetime.construct_from_aws(str(res.get('UserCreateDate'))), 3).utc()
        last_updated = round(LocalizedDatetime.construct_from_aws(str(res.get('UserLastModifiedDate'))), 3).utc()

        return cls(tag, password, invoice_number, created, last_updated)


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, None, None, None, None) if skeleton else None

        tag = jdict.get('username')
        password = jdict.get('password')

        invoice_number = jdict.get('invoice')

        created = LocalizedDatetime.construct_from_iso8601(jdict.get('created'))
        last_updated = LocalizedDatetime.construct_from_iso8601(jdict.get('last-updated'))

        return cls(tag, password, invoice_number, created, last_updated)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, password, invoice_number, created, last_updated):
        """
        Constructor
        """
        super().__init__(tag, password)

        self._invoice_number = invoice_number                   # string

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

        jdict['username'] = self.tag

        if self.password is not None:
            jdict['password'] = self.password

        jdict['invoice'] = self.invoice_number

        if self.created is not None:
            jdict['created'] = self.created.as_iso8601()

        if self.last_updated is not None:
            jdict['last-updated'] = self.last_updated.as_iso8601()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def invoice_number(self):
        return self._invoice_number


    @property
    def created(self):
        return self._created


    @property
    def last_updated(self):
        return self._last_updated


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoDeviceIdentity:{tag:%s, password:%s, invoice_number:%s, created:%s, last_updated:%s}" % \
               (self.tag, self.password, self.invoice_number, self.created, self.last_updated)
