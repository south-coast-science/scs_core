"""
Created on 22 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://docs.aws.amazon.com/cognito/latest/developerguide/signing-up-users-in-your-app.html
https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-policies.html
https://stackoverflow.com/questions/2520893/how-to-flush-the-input-stream-in-python

example document (credentials):
{"email": "production@southcoastscience.com", "password": "###", "retrieval-password": "###"}

example document (identity):
{"username": "8", "creation-date": "2021-11-24T12:51:12Z", "confirmation-status": "CONFIRMED", "enabled": true,
"email": "bruno.beloff@southcoastscience.com", "given-name": "Bruno", "family-name": "Beloff", "is-super": true}

example AWS response:
{"username": 22, "email": "bruno.beloff@southcoastscience.com", "given-name": "Bruno", "family-name": "Beloff",
"confirmation-status": "FORCE_CHANGE_PASSWORD", "enabled": true, "email-verified": false, "is-super": false,
"is-tester": false, "created": "2023-03-07T15:32:17Z", "last-updated": "2023-03-08T14:12:00Z"}
"""

import json
import sys
import termios

from collections import OrderedDict
from getpass import getpass

from scs_core.aws.security.cognito_user import CognitoUserCredentials, CognitoUserIdentity

from scs_core.data.datum import Datum
from scs_core.data.json import MultiPersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class CognitoClientUser(CognitoUserCredentials, MultiPersistentJSONable):
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
    def from_user(cls, name, existing_email=None):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)               # flush stdin
        except termios.error:
            pass

        if existing_email:
            email = existing_email

        else:
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
        CognitoUserCredentials.__init__(self, email, password)
        MultiPersistentJSONable.__init__(self, name)

        self.__retrieval_password = retrieval_password                  # string


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
    def retrieval_password(self):
        return self.__retrieval_password


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserCredentials:{name:%s, email:%s, password:%s, retrieval_password:%s}" %  \
               (self.name, self.email, self.password, self.retrieval_password)
