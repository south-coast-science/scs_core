"""
Created on 23 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from enum import Enum

from scs_core.aws.data.http_response import HTTPResponse

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class AuthenticationResult(HTTPResponse):
    """
    {"AccessToken": "...",
    "ExpiresIn": 3600,
    "TokenType": "Bearer",
    "RefreshToken": "...",
    "IdToken": "..."}
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_response_jdict(cls, status, jdict):
        if not jdict:
            return None

        # print(json.dumps(jdict, indent=4))

        authentication_status = AuthenticationStatus.construct_from_jdict(jdict.get('authentication-status'))

        if authentication_status == AuthenticationStatus.Ok:
            content = Session.construct_from_jdict(jdict.get('content').get('AuthenticationResult'))

        elif authentication_status == AuthenticationStatus.Challenge:
            content = Challenge.construct_from_jdict(jdict.get('content'))

        else:
            content = None

        return cls(status, authentication_status, content)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_status, authentication_status, content):
        """
        Constructor
        """
        super().__init__(http_status)

        self.__authentication_status = authentication_status            # AuthenticationStatus
        self.__content = content                                        # Session, Challenge or None


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['authentication-status'] = self.authentication_status
        jdict['content'] = self.content

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def is_ok(self):
        return self.authentication_status == AuthenticationStatus.Ok


    @property
    def id_token(self):
        if not self.is_ok():
            raise ValueError(self.authentication_status)

        return self.content.id_token


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def authentication_status(self):
        return self.__authentication_status


    @property
    def content(self):
        return self.__content


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AuthenticationResult:{http_status:%s, authentication_status:%s, content:%s}" % \
               (self.status, self.authentication_status, self.content)


# --------------------------------------------------------------------------------------------------------------------

class AuthenticationStatus(JSONable, Enum):
    """
    classdocs
    """

    Ok = (True, 'OK.')
    InvalidCredentials = (False, 'Invalid credentials.')
    Challenge = (False, 'Authentication challenge.')
    UserUnconfirmed = (False, 'User is unconfirmed.')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        return AuthenticationStatus[jdict]


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ok, description):
        self.__ok = ok                                      # bool
        self.__description = description                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.name


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def ok(self):
        return self.__ok


    @property
    def description(self):
        return self.__description


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AuthenticationStatus:{ok:%s, description:%s}" %  (self.ok, self.description)


# --------------------------------------------------------------------------------------------------------------------

class Challenge(JSONable):
    """
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        challenge_name = jdict.get('ChallengeName')
        session = jdict.get('Session')

        return cls(challenge_name, session)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, challenge_name, session):
        """
        Constructor
        """
        self.__challenge_name = challenge_name                  # string
        self.__session = session                                # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['ChallengeName'] = self.challenge_name
        jdict['Session'] = self.session

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def challenge_name(self):
        return self.__challenge_name


    @property
    def session(self):
        return self.__session


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Challenge:{challenge_name:%s, session:%s}" % \
               (self.challenge_name, self.session)


# --------------------------------------------------------------------------------------------------------------------

class Session(JSONable):
    """
    {"AccessToken": "...",
    "ExpiresIn": 3600,
    "TokenType": "Bearer",
    "RefreshToken": "...",
    "IdToken": "..."}
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        access_token = jdict.get('AccessToken')
        expires_in = jdict.get('ExpiresIn')
        token_type = jdict.get('TokenType')
        refresh_token = jdict.get('RefreshToken')
        id_token = jdict.get('IdToken')

        return cls(access_token, expires_in, token_type, refresh_token, id_token)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, access_token, expires_in, token_type, refresh_token, id_token):
        """
        Constructor
        """
        self.__access_token = access_token                      # string
        self.__expires_in = int(expires_in)                     # int
        self.__token_type = token_type                          # string
        self.__refresh_token = refresh_token                    # string
        self.__id_token = id_token                              # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['AccessToken'] = self.access_token
        jdict['ExpiresIn'] = self.expires_in
        jdict['TokenType'] = self.token_type
        jdict['RefreshToken'] = self.refresh_token
        jdict['IdToken'] = self.id_token

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def access_token(self):
        return self.__access_token


    @property
    def expires_in(self):
        return self.__expires_in


    @property
    def token_type(self):
        return self.__token_type


    @property
    def refresh_token(self):
        return self.__refresh_token


    @property
    def id_token(self):
        return self.__id_token


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Session:{access_token:%s, expires_in:%s, token_type:%s, refresh_token:%s, id_token:%s}" % \
               (self.access_token, self.expires_in, self.token_type, self.refresh_token, self.id_token)
