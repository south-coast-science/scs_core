"""
Created on 28 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
"""


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCheckRequester(object):
    """
    classdocs
    """

    __URL = "https://q272jk9le5.execute-api.us-west-2.amazonaws.com/default/MQTTConfigQueuer"


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, auth):
        self.__http_client = http_client
        self.__auth = auth


    # ----------------------------------------------------------------------------------------------------------------

    def request(self, tag):
        params = {'tag': tag}
        headers = {'Authorization': self.__auth.email_address}

        response = self.__http_client.get(self.__URL, headers=headers, params=params)

        return response


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationCheckRequester:{auth:%s}" % self.__auth
