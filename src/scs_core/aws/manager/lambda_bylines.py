"""
Created on 20 Sep 2022

@author: Jade Page (jade.page@southcoastscience.com)

Helper class for the bylines lambda
"""

import json

from collections import OrderedDict
from http import HTTPStatus

from scs_core.aws.data.http_response import HTTPResponse
from scs_core.client.http_exception import HTTPException


# ----------------------------------------------------------------------------------------------------------------

class BylineExclusiveStartKey(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        device = qsp.get('device')
        topic = qsp.get('topic')

        return cls(device, topic)


    @classmethod
    def construct_from_jdict(cls, jdict):
        return cls.construct_from_qsp(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, topic):
        """
        Constructor
        """
        self.__device = device                                      # string
        self.__topic = topic                                        # string


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            'device': self.device,
            'topic': self.topic
        }

        return params


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device(self):
        return self.__device


    @property
    def topic(self):
        return self.__topic


# --------------------------------------------------------------------------------------------------------------------


class BylineRequest(object):
    """
    classdocs
    """
    TAG_FILTER = 'device'
    TOPIC_FILTER = 'topic'
    EXCLUSIVE_START_KEY = 'exclusiveStartKey'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        tag_filter = qsp.get(cls.TAG_FILTER)
        topic_filter = qsp.get(cls.TOPIC_FILTER)

        esk_json = qsp.get(cls.EXCLUSIVE_START_KEY)
        exclusive_start_key = BylineExclusiveStartKey.construct_from_qsp(json.loads(esk_json)) if esk_json else None

        return cls(tag_filter, topic_filter, exclusive_start_key=exclusive_start_key)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag_filter, topic_filter, exclusive_start_key=None):
        """
        Constructor
        """
        self.__tag_filter = tag_filter  # string
        self.__topic_filter = topic_filter  # string

        self.__exclusive_start_key = exclusive_start_key  # ExclusiveStartKey


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {}

        if self.tag_filter is not None:
            params[self.TAG_FILTER] = self.tag_filter

        if self.topic_filter is not None:
            params[self.TOPIC_FILTER] = self.__topic_filter

        if self.exclusive_start_key is not None:
            params[self.EXCLUSIVE_START_KEY] = json.dumps(self.exclusive_start_key.params())

        return params

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag_filter(self):
        return self.__tag_filter


    @property
    def topic_filter(self):
        return self.__topic_filter


    @property
    def exclusive_start_key(self):
        return self.__exclusive_start_key


    @exclusive_start_key.setter
    def exclusive_start_key(self, exclusive_start_key):
        self.__exclusive_start_key = exclusive_start_key


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationRequest:{tag_filter:%s, topic_filter:%s, exclusive_start_key:%s}" % \
               (self.tag_filter, self.topic_filter, self.exclusive_start_key)


class BylinesResponse(HTTPResponse):
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

        items = jdict.get('Items')
        next_url = jdict.get('next')

        return cls(status, items, next_url=next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, items, next_url=None):
        """
        Constructor
        """
        super().__init__(status)

        self.__items = items  # list of string
        self.__next_url = next_url  # URL string


    def __len__(self):
        return len(self.items)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['statusCode'] = self.status.value

        if self.items is not None:
            jdict['Items'] = self.items
            jdict['itemCount'] = len(self.items)

        if self.next_url is not None:
            jdict['next'] = self.next_url

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def items(self):
        return self.__items


    @property
    def next_url(self):
        return self.__next_url


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BylinesResponse:{status:%s, items:%s, next_url:%s}" % \
               (self.status, self.items, self.next_url)
