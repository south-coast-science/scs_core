"""
Created on 07 Apr 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
"""

from collections import OrderedDict
from enum import Enum
from http import HTTPStatus

from scs_core.aws.data.http_response import HTTPResponse

from scs_core.data.str import Str

from scs_core.sample.configuration_sample import ConfigurationSample


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationFinder(object):
    """
    classdocs
    """

    __URL = "https://bwhogrzl3b.execute-api.us-west-2.amazonaws.com/default/MQTTDynamoHandler"


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, auth):
        self.__http_client = http_client
        self.__auth = auth


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, tag_filter, response_mode):
        # TODO: This is a temporary basic auth, will be updated with cognito pools prob
        headers = {'Authorization': 'scs123'}

        request = ConfigurationRequest(tag_filter, response_mode)
        response = self.__http_client.get(self.__URL, headers=headers, params=request.params())

        return ConfigurationResponse.construct_from_jdict(response.json())


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

        return True


    def tags_only(self):
        return self.__response_mode == self.MODE.TAGS_ONLY


    def history(self):
        return self.__response_mode == self.MODE.HISTORY


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            self.TAG_FILTER: self.tag_filter,
            self.RESPONSE_MODE: self.response_mode.name
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

class ConfigurationResponse(HTTPResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        status = HTTPStatus(jdict.get('statusCode'))

        try:
            mode = ConfigurationRequest.MODE[jdict.get('mode')]
        except KeyError:
            mode = None

        items = None
        if jdict.get('Items'):
            items = []
            for item_jdict in jdict.get('Items'):
                item = ConfigurationSample.construct_from_jdict(item_jdict)      # TODO: class depends on mode
                items.append(item)

        next_url = jdict.get('next')

        return cls(status, mode=mode, items=items, next_url=next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, mode=None, items=None, next_url=None):
        """
        Constructor
        """
        super().__init__(status)

        self.__mode = mode                              # ConfigurationRequest.Mode member
        self.__items = items                            # list of ConfigurationSample or string
        self.__next_url = next_url                      # URL string


    def __len__(self):
        return len(self.items)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['statusCode'] = self.status.value

        if not self.is_ok():
            return jdict

        if self.mode is not None:
            jdict['mode'] = self.mode.name

        if self.items is not None:
            jdict['Items'] = self.items
            jdict['itemCount'] = len(self.items)

        if self.next_url is not None:
            jdict['next'] = self.next_url

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mode(self):
        return self.__mode


    @property
    def items(self):
        return self.__items


    @property
    def next_url(self):
        return self.__next_url


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationResponse:{status:%s, mode:%s, items:%s, next_url:%s}" % \
               (self.status, self.mode, Str.collection(self.items), self.next_url)
