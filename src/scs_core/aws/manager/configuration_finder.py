"""
Created on 07 Apr 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

from enum import Enum

# from scs_core.estate.configuration import Configuration


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationFinder(object):
    """
    classdocs
    """

    __URL = "https://bwhogrzl3b.execute-api.us-west-2.amazonaws.com/default/MQTTDynamoHandler"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_lib, auth):
        self.__http_lib = http_lib
        self.__auth = auth


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, tag_filter, response_mode):
        # TODO: This is a temporary basic auth, will be updated with cognito pools prob
        headers = {'Authorization': 'scs123'}
        request = ConfigurationRequest(tag_filter, response_mode)
        print(request)
        data = self.__http_lib.get(self.__URL, headers=headers, params=request.params())

        if data.status_code != 400:
            if data.status_code == 403:
                return 1
            if data.status_code == 401:
                return 2
            else:
                return 3

        j_data = data.json()

        return j_data


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationFinder:{auth:%s}" % self.__auth


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationRequest(object):
    """
    classdocs
    """

    MODE = Enum('Mode', 'FULL TAGS_ONLY HISTORY')

    TAG_FILTER = 'tagFilter'
    RESPONSE_MODE = 'responseMode'


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        # compulsory...
        tag_filter = qsp.get(cls.TAG_FILTER)

        try:
            response_mode = cls.MODE[qsp.get(cls.RESPONSE_MODE)]
        except KeyError:
            response_mode = None

        return cls(tag_filter, response_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag_filter, response_mode):
        """
        Constructor
        """
        self.__tag_filter = tag_filter                          # string
        self.__response_mode = response_mode                    # MODE enum


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.response_mode is None:
            return False


    def tags_only(self):
        return self.__response_mode == self.MODE.TAGS_ONLY


    def history(self):
        return self.__response_mode == self.MODE.HISTORY


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            self.TAG_FILTER: self.tag_filter,
            self.RESPONSE_MODE: self.response_mode
        }

        return params


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag_filter(self):
        return self.__tag_filter


    @property
    def response_mode(self):
        return self.__response_mode


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationRequest:{tag_filter:%s, response_mode:%s}" % \
               (self.tag_filter, self.response_mode)


# --------------------------------------------------------------------------------------------------------------------

