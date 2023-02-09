"""
Created on 9 Feb 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

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

    def resend_confirmation(self, email):
        url = '/'.join((self.__URL, 'resend-confirmation'))
        payload = {'email': email}

        response = self.__http_client.post(url, headers=self.__HEADERS, data=JSONify.dumps(payload))
        status = HTTPStatus(response.status_code)

        logging.info('resend_confirmation - status_code: %s' % response.status_code)
        logging.info('resend_confirmation - text: %s' % response.text)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    def resend_temporary_password(self, email):
        url = '/'.join((self.__URL, 'resend-temporary'))
        payload = {'email': email}

        response = self.__http_client.post(url, headers=self.__HEADERS, data=JSONify.dumps(payload))
        status = HTTPStatus(response.status_code)

        logging.info('resend_temporary_password - status_code: %s' % response.status_code)
        logging.info('resend_temporary_password - text: %s' % response.text)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    def request_reset_password(self, email):
        url = '/'.join((self.__URL, 'request'))
        payload = {'email': email}

        response = self.__http_client.post(url, headers=self.__HEADERS, data=JSONify.dumps(payload))
        status = HTTPStatus(response.status_code)

        logging.info('request_reset_password - status_code: %s' % response.status_code)
        logging.info('request_reset_password - text: %s' % response.text)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    def do_reset_password(self, email, code, password):
        url = '/'.join((self.__URL, 'reset'))
        payload = {'email': email, 'reset_code': code, 'new_password': password}

        response = self.__http_client.post(url, headers=self.__HEADERS, data=JSONify.dumps(payload))
        status = HTTPStatus(response.status_code)

        logging.info('do_reset_password - status_code: %s' % response.status_code)
        logging.info('do_reset_password - text: %s' % response.text)

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
