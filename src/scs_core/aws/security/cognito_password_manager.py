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

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class CognitoPasswordManager(APIClient):
    """
    classdocs
    """

    __URL = "https://df46l72wl7.execute-api.us-west-2.amazonaws.com/default/CognitoUserPassword"
    __AUTH = "@southcoastscience.com"


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def send_email(self, email):
        url = '/'.join((self.__URL, 'send-email'))
        payload = {'email': email}

        response = requests.post(url, headers=self._auth_headers(self.__AUTH), data=JSONify.dumps(payload))
        self._check_response(response)


    def do_reset_password(self, email, code, new_password):
        url = '/'.join((self.__URL, 'reset'))
        payload = {'email': email, 'reset_code': code, 'new_password': new_password}

        response = requests.post(url, headers=self._auth_headers(self.__AUTH), data=JSONify.dumps(payload))
        self._check_response(response)


    def do_set_password(self, email, new_password, session):
        url = '/'.join((self.__URL, 'respond'))
        payload = {'email': email, 'new_password': new_password, 'session': session}

        response = requests.post(url, headers=self._auth_headers(self.__AUTH), data=JSONify.dumps(payload))
        self._check_response(response)
