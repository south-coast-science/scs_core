"""
Created on 9 Feb 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

* resend_confirmation - re-send confirmation email when account is created using the API
* resend_temporary_password - re-send temporary password that was created by the security_import system
* request_reset_password - re-send a code needed to do a password reset
* do_reset_password - perform a password reset using the code
* do_set_password - change password when in force reset mode created by security_import system

https://docs.python.org/3/howto/enum.html#planet

document example:
"EmailSent"
"""

import logging

from enum import Enum
from http import HTTPStatus

from scs_core.data.json import JSONable, JSONify

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class CognitoPasswordManager(object):
    """
    classdocs
    """

    __URL = "https://df46l72wl7.execute-api.us-west-2.amazonaws.com/default/CognitoUserPassword"

    __HEADERS = {'Content-type': 'application/x-www-form-urlencoded',
                 'Accept': 'text/plain', 'Authorization': '@southcoastscience.com'}


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        self.__http_client = http_client                # requests package
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def send_email(self, email):
        url = '/'.join((self.__URL, 'send-email'))
        payload = {'email': email}

        response = self.__http_client.post(url, headers=self.__HEADERS, data=JSONify.dumps(payload))
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    def do_reset_password(self, email, code, new_password):
        url = '/'.join((self.__URL, 'reset'))
        payload = {'email': email, 'reset_code': code, 'new_password': new_password}

        response = self.__http_client.post(url, headers=self.__HEADERS, data=JSONify.dumps(payload))
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    def do_set_password(self, email, new_password, session):
        url = '/'.join((self.__URL, 'respond'))
        payload = {'email': email, 'new_password': new_password, 'session': session}

        response = self.__http_client.post(url, headers=self.__HEADERS, data=JSONify.dumps(payload))
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoPasswordManager:{}"


# --------------------------------------------------------------------------------------------------------------------

class CognitoPasswordResponse(JSONable, Enum):
    """
    classdocs
    """

    Ok = (True, 'OK.')
    EmailSent = (True, 'Email sent.')
    InvalidEmail = (False, 'Invalid email address.')
    UnknownUser = (False, 'Unknown user.')
    CannotSendInStateU = (False, 'Email cannot be sent in state UNCONFIRMED.')
    CannotSendInStateC = (False, 'Email cannot be sent in state CONFIRMED.')
    CannotSendInStateP = (False, 'Email cannot be sent in state PASSWORD_RESET_REQUIRED.')
    CannotSendInStateF = (False, 'Email cannot be sent in state FORCE_CHANGE_PASSWORD.')
    CannotSendInStateD = (False, 'Email cannot be sent in state DISABLED.')
    UnknownResetCode = (False, 'Unknown reset code.')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        return CognitoPasswordResponse[jdict]


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
        return "CognitoPasswordResponse:{ok:%s, description:%s}" %  (self.ok, self.description)
