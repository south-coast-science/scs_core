"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.aws.data.http_response import HTTPResponse


# --------------------------------------------------------------------------------------------------------------------

class CognitoCreateManager(object):
    """
    classdocs
    """

    __AUTHORIZATION = 'southcoastscience.com'
    __URL = 'https://85nkjtux72.execute-api.us-west-2.amazonaws.com/default/CognitoAccountCreator'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        self.__http_client = http_client                # requests package


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, identity):
        headers = {'Authorization': self.__AUTHORIZATION}
        response = self.__http_client.post(self.__URL, headers=headers, json=identity.as_json())

        print("status_code: %s" % response.status_code)
        print("text: %s" % response.text)

        # return CognitoAuthenticationResult.construct_from_response(response)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoCreateManager:{}"


# --------------------------------------------------------------------------------------------------------------------

class CognitoUpdateManager(object):
    """
    classdocs
    """

    __URL = 'https://x45yjp88e2.execute-api.us-west-2.amazonaws.com/default/CognitoAccounts/edit'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, id_token):
        self.__http_client = http_client                    # requests package
        self.__id_token = id_token                          # string


    # ----------------------------------------------------------------------------------------------------------------

    def update(self, identity):
        headers = {'Token': self.__id_token}
        response = self.__http_client.patch(self.__URL, headers=headers, data=identity.as_json())

        print("status_code: %s" % response.status_code)
        print("text: %s" % response.text)

        # return CognitoAuthenticationResult.construct_from_response(response)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUpdateManager:{id_token:%s}" % self.__id_token
