"""
Created on 1 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Equivalent to cURLs:
curl "https://aws.southcoastscience.com/device-topics?topic=south-coast-science-dev/alphasense/loc/303/gases"
curl "https://aws.southcoastscience.com/device-topics?device=scs-bgx-303"
"""

import requests

from collections import OrderedDict
from urllib.parse import parse_qs, urlparse

from scs_core.aws.client.api_client import APIClient, APIResponse
from scs_core.aws.data.byline import Byline, DeviceBylineGroup, TopicBylineGroup

from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class BylineFinder(APIClient):
    """
    classdocs
    """

    __URL = 'https://k5uz49605m.execute-api.us-west-2.amazonaws.com/default/TopicBylines'

    __DEVICE =      'device'
    __TOPIC =       'topic'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reporter=None):
        super().__init__(reporter=reporter)


    # ----------------------------------------------------------------------------------------------------------------

    def find_latest_byline_for_topic(self, token, topic):
        params = {self.__TOPIC: topic}

        response = requests.get(self.__URL, headers=self._token_headers(token), params=params)
        jdict = response.json()

        # bylines...
        if jdict is None:
            return None

        latest_byline = None

        for item in jdict:
            byline = Byline.construct_from_jdict(item)

            if latest_byline is None or latest_byline.rec < byline.rec:
                latest_byline = byline

        return latest_byline


    def find_bylines(self, token, excluded=None, strict_tags=False):
        bylines = [item for item in self._get_blocks(self.__URL, token, BylineFinderResponse)]

        return TopicBylineGroup.construct(bylines, excluded=excluded, strict_tags=strict_tags)


    def find_bylines_for_topic(self, token, topic, excluded=None, strict_tags=False):
        params = {self.__TOPIC: topic}

        response = requests.get(self.__URL, headers=self._token_headers(token), params=params)
        self._check_response(response)

        jdict = response.json()

        # bylines...
        return TopicBylineGroup.construct_from_jdict(jdict, excluded=excluded, strict_tags=strict_tags, skeleton=True)


    def find_bylines_for_device(self, token, device, excluded=None):
        params = {self.__DEVICE: device}

        response = requests.get(self.__URL, headers=self._token_headers(token), params=params)
        self._check_response(response)

        jdict = response.json()

        # bylines...
        return DeviceBylineGroup.construct_from_jdict(jdict, excluded=excluded, skeleton=True)


# --------------------------------------------------------------------------------------------------------------------

class DeviceBylineFinder(APIClient):
    """
    classdocs
    """

    __URL = 'https://k5uz49605m.execute-api.us-west-2.amazonaws.com/default/TopicBylines/self'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find_byline_for_topic(self, token, topic):
        response = requests.get(self.__URL, headers=self._token_headers(token))
        self._check_response(response)

        jdict = response.json()

        # bylines...
        if jdict is None:
            return None

        for item in jdict:
            byline = Byline.construct_from_jdict(item)

            if byline.topic == topic:
                return byline

        return None


# --------------------------------------------------------------------------------------------------------------------

class BylineFinderResponse(APIResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        items = []
        if jdict.get('Items'):
            for item_jdict in jdict.get('Items'):
                item = Byline.construct_from_jdict(item_jdict)
                items.append(item)

        next_url = jdict.get('next')

        return cls(items, next_url=next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items, next_url=None):
        """
        Constructor
        """
        self.__items = items                                # list of Byline
        self.__next_url = next_url                          # URL string


    def __len__(self):
        return len(self.items)


    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, _):
        return parse_qs(urlparse(self.next_url).query)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

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
        return "BylineFinderResponse:{items:%s, next_url:%s}" %  (Str.collection(self.items), self.next_url)
