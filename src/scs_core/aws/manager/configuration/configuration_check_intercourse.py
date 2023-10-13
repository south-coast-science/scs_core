"""
Created on 2 Oct 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
"""

from collections import OrderedDict
from enum import Enum
from http import HTTPStatus

from scs_core.aws.data.http_response import HTTPResponse

from scs_core.client.http_exception import HTTPException
from scs_core.data.str import Str
from scs_core.data.datum import Datum
from scs_core.estate.configuration_check import ConfigurationCheck


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCheckRequest(object):
    """
    classdocs
    """

    class Mode(Enum):
        FULL = 1
        TAGS_ONLY = 2

    TAG_FILTER = 'tagFilter'
    EXACT_MATCH = 'exactMatch'
    RESPONSE_MODE = 'responseMode'


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        tag_filter = qsp.get(cls.TAG_FILTER)
        exact_match = Datum.is_true(qsp.get(cls.EXACT_MATCH))

        try:
            response_mode = cls.Mode[qsp.get(cls.RESPONSE_MODE)]
        except KeyError:
            response_mode = None

        return cls(tag_filter, exact_match, response_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag_filter, exact_match, response_mode):
        """
        Constructor
        """
        self.__tag_filter = tag_filter                          # string
        self.__exact_match = bool(exact_match)                  # bool
        self.__response_mode = response_mode                    # MODE enum


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.response_mode is None:
            return False

        return True


    def tags_only(self):
        return self.__response_mode == self.Mode.TAGS_ONLY


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            self.TAG_FILTER: self.tag_filter,
            self.EXACT_MATCH: self.exact_match,
            self.RESPONSE_MODE: self.response_mode.name
        }

        return params


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag_filter(self):
        return self.__tag_filter


    @property
    def exact_match(self):
        return self.__exact_match


    @property
    def response_mode(self):
        return self.__response_mode


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationCheckRequest:{tag_filter:%s, exact_match:%s, response_mode:%s}" % \
               (self.tag_filter, self.exact_match, self.response_mode)


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCheckResponse(HTTPResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        status = HTTPStatus(jdict.get('statusCode'))

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, status.phrase, status.description)

        mode = ConfigurationCheckRequest.Mode[jdict.get('mode')]

        items = []
        if jdict.get('Items'):
            for item_jdict in jdict.get('Items'):
                item = item_jdict.get('tag') if mode == ConfigurationCheckRequest.Mode.TAGS_ONLY else \
                    ConfigurationCheck.construct_from_jdict(item_jdict)
                items.append(item)

        next_url = jdict.get('next')

        return cls(status, mode, items, next_url=next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, mode, items, next_url=None):
        """
        Constructor
        """
        super().__init__(status)

        self.__mode = mode                              # ConfigurationCheckRequest.Mode member
        self.__items = items                            # list of ConfigurationCheck or string
        self.__next_url = next_url                      # URL string


    def __len__(self):
        return len(self.items)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['statusCode'] = self.status.value

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
        return "ConfigurationCheckResponse:{status:%s, mode:%s, items:%s, next_url:%s}" % \
               (self.status, self.mode, Str.collection(self.items), self.next_url)
