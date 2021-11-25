"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.security.cognito_user import CognitoUserIdentity


# --------------------------------------------------------------------------------------------------------------------

class CognitoFinder(object):
    """
    classdocs
    """

    __URL = 'https://unnyezcdaa.execute-api.us-west-2.amazonaws.com/default/CognitoFinder'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, id_token):
        self.__http_client = http_client                    # requests package
        self.__id_token = id_token                          # string


    # ----------------------------------------------------------------------------------------------------------------

    def find_all(self):
        url = '/'.join((self.__URL, 'all'))
        headers = {'Token': self.__id_token}

        response = self.__http_client.get(url, headers=headers)

        print("status_code: %s" % response.status_code)
        print("text: %s" % response.text)

        return [CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json()]


    def find_by_email(self, email):
        url = '/'.join((self.__URL, email))
        headers = {'Token': self.__id_token}

        response = self.__http_client.get(url, headers=headers)

        print("status_code: %s" % response.status_code)
        print("text: %s" % response.text)

        return [CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json()]


    def find_self(self):
        url = '/'.join((self.__URL, 'self'))
        headers = {'Token': self.__id_token}

        response = self.__http_client.get(url, headers=headers)

        return CognitoUserIdentity.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoFinder:{id_token:%s}" % self.__id_token
