"""
Created on 22 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://docs.aws.amazon.com/cognito/latest/developerguide/signing-up-users-in-your-app.html
https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-policies.html
https://stackoverflow.com/questions/2520893/how-to-flush-the-input-stream-in-python

example document (credentials):
{"email": "bruno.beloff@southcoastscience.com", "password": "pass"}

example document (identity):
{"username": "8", "creation-date": "2021-11-24T12:51:12Z", "confirmation-status": "CONFIRMED", "enabled": true,
"email": "bruno.beloff@southcoastscience.com", "given-name": "Bruno", "family-name": "Beloff", "is-super": true}

example AWS response:
{'Username': '1092', 'Attributes': [{'Name': 'sub', 'Value': '332351ef-f74f-4cb4-aec8-664a3a9abae3'},
{'Name': 'custom:tester', 'Value': 'False'}, {'Name': 'custom:super', 'Value': 'False'},
{'Name': 'email', 'Value': 'adrian@em-monitors.co.uk'}],
'UserCreateDate': datetime.datetime(2023, 1, 20, 9, 14, 22, 821000, tzinfo=tzlocal()),
'UserLastModifiedDate': datetime.datetime(2023, 1, 20, 9, 14, 22, 821000, tzinfo=tzlocal()),
'Enabled': True, 'UserStatus': 'FORCE_CHANGE_PASSWORD'}
"""

import json
import re
import sys
import termios

from collections import OrderedDict
from getpass import getpass

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable, MultiPersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserCredentials(MultiPersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "cognito_user_credentials.json"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def from_stdin(cls, name):
        line = sys.stdin.readline()
        jdict = json.loads(line)

        return cls.construct_from_jdict(jdict, name=name)


    @classmethod
    def from_user(cls, name):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)               # flush stdin
        except termios.error:
            pass

        print("Enter email address: ", end="", file=sys.stderr)
        email = input().strip()

        print("Enter password: ", end="", file=sys.stderr)
        password = input().strip()

        print("Enter retrieval password (RETURN for same): ", end="", file=sys.stderr)
        retrieval_password = input().strip()

        if not retrieval_password:
            retrieval_password = password

        return cls(name, email, password, retrieval_password)


    @staticmethod
    def password_from_user():
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)               # flush stdin
        except termios.error:
            pass

        return getpass().strip()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))

        return cls.aws_dir(), filename


    @classmethod
    def construct_from_jdict(cls, jdict, name=None, skeleton=False):
        if not jdict:
            return cls(None, None, None, None) if skeleton else None

        email = jdict.get('email')
        password = jdict.get('password')
        retrieval_password = jdict.get('retrieval-password')

        return cls(name, email, password, retrieval_password)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, email, password, retrieval_password):
        """
        Constructor
        """
        super().__init__(name)

        self.__email = email                                        # string (email)
        self.__password = password                                  # string (AWS password)
        self.__retrieval_password = retrieval_password              # string


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

    def as_json(self):
        jdict = OrderedDict()

        jdict['email'] = self.email
        jdict['password'] = self.password
        jdict['retrieval-password'] = self.retrieval_password

        return jdict


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


    @property
    def retrieval_password(self):
        return self.__retrieval_password


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserCredentials:{name:%s, email:%s, password:%s, retrieval_password:%s}" %  \
               (self.name, self.email, self.password, self.retrieval_password)


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


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, None, None, None, None, None, None, None) if skeleton else None

        username = jdict.get('username')
        created = LocalizedDatetime.construct_from_iso8601(jdict.get('created'))
        confirmation_status = jdict.get('confirmation_status')
        enabled = jdict.get('enabled')
        email = jdict.get('email')
        given_name = jdict.get('given_name')
        family_name = jdict.get('family_name')
        password = jdict.get('password')
        is_super = jdict.get('is_super') == 'True'
        is_tester = jdict.get('is_tester') == 'True'

        return cls(username, created, confirmation_status, enabled,
                   email, given_name, family_name, password, is_super=is_super, is_tester=is_tester)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, created, confirmation_status, enabled,
                 email, given_name, family_name, password, is_super=False, is_tester=False):
        """
        Constructor
        """
        # TODO: Why force int?
        self.__username = username
        self._created = created                                 # LocalisedDatetime
        self.__confirmation_status = confirmation_status        # string
        self.__enabled = Datum.bool(enabled)                    # bool or None
        self.__email = email                                    # string
        self.__given_name = given_name                          # string
        self.__family_name = family_name                        # string
        self.__password = password                              # string
        self.__is_super = bool(is_super)                        # bool
        self.__is_tester = bool(is_tester)


    def __eq__(self, other):
        try:
            return self.username == other.username and self.confirmation_status == other.confirmation_status \
                   and self.enabled == other.enabled and self.email == other.email \
                   and self.given_name == other.given_name and self.family_name == other.family_name \
                   and self.is_super == other.is_super

        except (TypeError, AttributeError):
            return False


    def __lt__(self, other):
        if self.family_name is not None:
            if other.family_name is None:
                return False

            if self.family_name.lower() < other.family_name.lower():
                return True

            if self.family_name.lower() > other.family_name.lower():
                return False

        if self.given_name is not None:
            if other.given_name is None:
                return False

            if self.given_name.lower() < other.given_name.lower():
                return True

            if self.given_name.lower() > other.given_name.lower():
                return False

        if self.email.lower() < other.email.lower():
            return True

        if self.email.lower() > other.email.lower():
            return False

        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def index(self):
        return self.email


    @property
    def latest_update(self):                    # LocalizedDatetime
        return None


    def copy_id(self, other):
        pass


    def save(self, db_user):
        raise NotImplementedError


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.username is not None:
            jdict['username'] = self.username

        if self.created is not None:
            jdict['created'] = self.created.as_iso8601()

        if self.confirmation_status is not None:
            jdict['confirmation_status'] = self.confirmation_status

        if self.enabled is not None:
            jdict['enabled'] = self.enabled

        jdict['email'] = self.email

        if self.password is not None:
            jdict['password'] = self.password

        jdict['given_name'] = self.given_name
        jdict['family_name'] = self.family_name
        jdict['is_super'] = self.is_super
        jdict['is_tester'] = self.is_tester

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.__username


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

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserIdentity:{username:%s, created:%s, confirmation_status:%s, enabled:%s, " \
               "email:%s, given_name:%s, family_name:%s, is_super:%s, is_tester:%s}" % \
               (self.username, self.created, self.confirmation_status, self.enabled,
                self.email, self.given_name, self.family_name, self.is_super, self.is_tester)
