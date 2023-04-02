"""
Created on 22 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://docs.aws.amazon.com/cognito/latest/developerguide/signing-up-users-in-your-app.html
https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-policies.html

example document (identity):
{"username": "8", "creation-date": "2021-11-24T12:51:12Z", "confirmation-status": "CONFIRMED", "enabled": true,
"email": "bruno.beloff@southcoastscience.com", "given-name": "Bruno", "family-name": "Beloff", "is-super": true}

example AWS response:
{"username": 22, "email": "bruno.beloff@southcoastscience.com", "given-name": "Bruno", "family-name": "Beloff",
"confirmation-status": "FORCE_CHANGE_PASSWORD", "enabled": true, "email-verified": false, "is-super": false,
"is-tester": false, "created": "2023-03-07T15:32:17Z", "last-updated": "2023-03-08T14:12:00Z"}
"""

import re

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserCredentials(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, email, password):
        """
        Constructor
        """
        self.__email = email                                        # string (email)
        self.__password = password                                  # string (AWS password)


    # ----------------------------------------------------------------------------------------------------------------

    def ok(self):
        if not self.email or not self.password:
            return False

        if not Datum.is_email_address(self.email):
            return False

        if not CognitoUserIdentity.is_valid_password(self.password):
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def email(self):
        return self.__email


    @email.setter
    def email(self, email):
        self.__email = email


    @property
    def password(self):
        return self.__password


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserCredentials:{email:%s, password:%s}" %  (self.email, self.password)


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserIdentity(JSONable):
    """
    classdocs
    """

    __STATUSES = {
        'U': 'UNCONFIRMED',
        'C': 'CONFIRMED',
        'P': 'PASSWORD_RESET_REQUIRED',
        'F': 'FORCE_CHANGE_PASSWORD',
        'D': 'DISABLED'
    }

    @classmethod
    def status_codes(cls):
        return cls.__STATUSES.keys()


    @classmethod
    def status(cls, code):
        return cls.__STATUSES[code]


    __EMAIL_FUNCTIONS = {
        'UNCONFIRMED': 'RESEND_CONFIRMATION',
        'CONFIRMED': 'REQUEST_PASSWORD_RESET',
        'PASSWORD_RESET_REQUIRED': 'REQUEST_PASSWORD_RESET',
        'FORCE_CHANGE_PASSWORD': 'RESEND_TEMPORARY_PASSWORD',
        'DISABLED': None
    }


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def is_valid_password(password):
        if not isinstance(password, str):
            return False

        if not 7 < len(password) < 99:
            return False

        if not re.findall(r'[0-9]', password):
            return False

        if not re.findall(r'[A-Z]', password):
            return False

        if not re.findall(r'[a-z]', password):
            return False

        if not re.findall(r'[\^$*.\[\]{}()?"!@#%&/\\,><\':;|_~`]', password):
            return False

        return True


    @staticmethod
    def ext_name(name):
        return '-' if name is None or name.strip() == '' else name


    @staticmethod
    def int_name(name):
        return None if name == '-' else name


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, None, None, None, None, None, None, None, None, None, None, None) if skeleton else None

        username = jdict.get('username')
        email = jdict.get('email')
        password = jdict.get('password')
        given_name = cls.int_name(jdict.get('given-name'))
        family_name = cls.int_name(jdict.get('family-name'))

        confirmation_status = jdict.get('confirmation-status')
        enabled = jdict.get('enabled')
        email_verified = jdict.get('email-verified')
        is_super = jdict.get('is-super')
        is_tester = jdict.get('is-tester')

        created = LocalizedDatetime.construct_from_iso8601(jdict.get('created'))
        last_updated = LocalizedDatetime.construct_from_iso8601(jdict.get('last-updated'))

        return cls(username, created, confirmation_status, enabled,
                   email_verified, email, given_name, family_name, password, is_super, is_tester, last_updated)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, created, confirmation_status, enabled,
                 email_verified, email, given_name, family_name, password, is_super, is_tester, last_updated):
        """
        Constructor
        """

        self._username = username                                   # string email address or hash
        self._created = created                                     # LocalisedDatetime
        self.__confirmation_status = confirmation_status            # string
        self.__enabled = Datum.bool(enabled)                        # bool or None

        self.__email_verified = bool(email_verified)                # bool
        self.__email = email                                        # string
        self.__given_name = given_name                              # string
        self.__family_name = family_name                            # string
        self.__password = password                                  # string
        self.__is_super = bool(is_super)                            # bool
        self.__is_tester = bool(is_tester)                          # bool

        self._last_updated = last_updated                           # LocalizedDatetime


    def __eq__(self, other):
        try:
            return self.username == other.username and self.confirmation_status == other.confirmation_status \
                   and self.enabled == other.enabled and self.email_verified == other.email_verified \
                   and self.email == other.email and self.given_name == other.given_name \
                   and self.family_name == other.family_name and self.is_super == other.is_super \
                   and self.is_tester == other.is_tester

        except (TypeError, AttributeError):
            return False


    def __lt__(self, other):
        # family_name...
        self_name = self.ext_name(self.family_name)
        other_name = self.ext_name(other.family_name)

        if self_name.lower() < other_name.lower():
            return True

        if self_name.lower() > other_name.lower():
            return False

        # given_name...
        self_name = self.ext_name(self.given_name)
        other_name = self.ext_name(other.given_name)

        if self_name.lower() < other_name.lower():
            return True

        if self_name.lower() > other_name.lower():
            return False

        # email...
        if self.email.lower() < other.email.lower():
            return True

        if self.email.lower() > other.email.lower():
            return False

        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def index(self):
        return self.email


    def copy_id(self, other):
        pass


    def save(self, db_user):
        raise NotImplementedError


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def email_function(self):
        try:
            return self.__EMAIL_FUNCTIONS[self.confirmation_status]

        except KeyError:
            raise ValueError(self.confirmation_status)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.username is not None:
            jdict['username'] = self.username

        jdict['email'] = self.email

        if self.password is not None:
            jdict['password'] = self.password

        jdict['given-name'] = self.ext_name(self.given_name)
        jdict['family-name'] = self.ext_name(self.family_name)

        if self.confirmation_status is not None:
            jdict['confirmation-status'] = self.confirmation_status

        if self.enabled is not None:
            jdict['enabled'] = self.enabled

        jdict['email-verified'] = self.email_verified
        jdict['is-super'] = self.is_super
        jdict['is-tester'] = self.is_tester

        if self.created is not None:
            jdict['created'] = self.created.as_iso8601()

        if self.last_updated is not None:
            jdict['last-updated'] = self.last_updated.as_iso8601()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self._username


    @property
    def created(self):
        return self._created


    @property
    def confirmation_status(self):
        return self.__confirmation_status


    @property
    def enabled(self):
        return self.__enabled


    @property
    def email_verified(self):
        return self.__email_verified


    @property
    def email(self):
        return self.__email


    @property
    def given_name(self):
        return self.__given_name


    @property
    def family_name(self):
        return self.__family_name


    @property
    def password(self):
        return self.__password


    @property
    def is_super(self):
        return self.__is_super


    @property
    def is_tester(self):
        return self.__is_tester


    @property
    def last_updated(self):
        return self._last_updated


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{username:%s, created:%s, confirmation_status:%s, enabled:%s, " \
               "email_verified:%s, email:%s, given_name:%s, family_name:%s, is_super:%s, is_tester:%s, " \
               "last_updated:%s}" % \
               (self.username, self.created, self.confirmation_status, self.enabled,
                self.email_verified, self.email, self.given_name, self.family_name, self.is_super, self.is_tester,
                self.last_updated)
