"""
Created on 07 Apr 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
"""

import json

from collections import OrderedDict
from enum import Enum
from urllib.parse import parse_qs, urlparse

from scs_core.aws.client.api_intercourse import APIResponse

from scs_core.data.str import Str
from scs_core.data.datum import Datum

from scs_core.sample.configuration_sample import ConfigurationSample


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationRequest(object):
    """
    classdocs
    """

    class Mode(Enum):
        LATEST = 1
        HISTORY = 2
        DIFF = 3
        TAGS_ONLY = 4

    TAG_FILTER = 'tagFilter'
    EXACT_MATCH = 'exactMatch'
    RESPONSE_MODE = 'responseMode'
    EXCLUSIVE_START_KEY = 'exclusiveStartKey'

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

        esk_json = qsp.get(cls.EXCLUSIVE_START_KEY)
        exclusive_start_key = ExclusiveStartKey.construct_from_qsp(json.loads(esk_json)) if esk_json else None

        return cls(tag_filter, exact_match, response_mode, exclusive_start_key=exclusive_start_key)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag_filter, exact_match, response_mode, exclusive_start_key=None):
        """
        Constructor
        """
        self.__tag_filter = tag_filter                          # string
        self.__exact_match = bool(exact_match)                  # bool
        self.__response_mode = response_mode                    # Mode enum

        self.__exclusive_start_key = exclusive_start_key        # ExclusiveStartKey


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.response_mode is None:
            return False

        return True


    def latest(self):
        return self.__response_mode == self.Mode.LATEST


    def history(self):
        return self.__response_mode == self.Mode.HISTORY


    def diff(self):
        return self.__response_mode == self.Mode.DIFF


    def tags_only(self):
        return self.__response_mode == self.Mode.TAGS_ONLY


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            self.EXACT_MATCH: self.exact_match,
            self.RESPONSE_MODE: self.response_mode.name
        }

        if self.tag_filter is not None:
            params[self.TAG_FILTER] = self.tag_filter

        if self.exclusive_start_key is not None:
            params[self.EXCLUSIVE_START_KEY] = json.dumps(self.exclusive_start_key.params())

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


    @property
    def exclusive_start_key(self):
        return self.__exclusive_start_key


    @exclusive_start_key.setter
    def exclusive_start_key(self, exclusive_start_key):
        self.__exclusive_start_key = exclusive_start_key


    @property
    def exclusive_start_key_params(self):
        return self.__exclusive_start_key.params() if self.__exclusive_start_key else None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationRequest:{tag_filter:%s, exact_match:%s, response_mode:%s, exclusive_start_key:%s}" % \
               (self.tag_filter, self.exact_match, self.response_mode, self.exclusive_start_key)


# --------------------------------------------------------------------------------------------------------------------

class ExclusiveStartKey(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        rec = qsp.get('rec')
        tag = qsp.get('tag')

        return cls(rec, tag)


    @classmethod
    def construct_from_jdict(cls, jdict):
        return cls.construct_from_qsp(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, tag):
        """
        Constructor
        """
        self.__rec = rec                    # string
        self.__tag = tag                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {'tag': self.tag}

        if self.rec is not None:
            params['rec'] = self.rec

        return params


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def tag(self):
        return self.__tag


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ExclusiveStartKey:{rec:%s, tag:%s}" %  (self.rec, self.tag)


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationResponse(APIResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        mode = ConfigurationRequest.Mode[jdict.get('mode')]

        items = []
        if jdict.get('Items'):
            for item_jdict in jdict.get('Items'):
                item = item_jdict if mode == ConfigurationRequest.Mode.TAGS_ONLY else  \
                    ConfigurationSample.construct_from_jdict(item_jdict)
                items.append(item)

        next_url = jdict.get('next')

        return cls(mode, items, next_url=next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mode, items, next_url=None):
        """
        Constructor
        """
        self.__mode = mode                                  # ConfigurationRequest.Mode member
        self.__items = items                                # list of ConfigurationSample or string
        self.__next_url = next_url                          # URL string


    def __len__(self):
        return len(self.items)


    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, _):
        return parse_qs(urlparse(self.next_url).query)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

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
        return "ConfigurationResponse:{mode:%s, items:%s, next_url:%s}" % \
               (self.mode, Str.collection(self.items), self.next_url)
