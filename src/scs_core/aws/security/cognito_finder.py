"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class CognitoFinder(object):
    """
    classdocs
    """

    __AUTHORIZATION = 'southcoastscience.com'
    __URL = 'https://unnyezcdaa.execute-api.us-west-2.amazonaws.com/default/CognitoFinder/any'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        self.__http_client = http_client                # requests package


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, id_token):
        headers = {'Token': id_token}
        response = self.__http_client.get(self.__URL, headers=headers)

        print("status_code: %s" % response.status_code)
        print("text: %s" % response.text)

        # return CognitoAuthenticationResult.construct_from_response(response)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoFinder:{}"
