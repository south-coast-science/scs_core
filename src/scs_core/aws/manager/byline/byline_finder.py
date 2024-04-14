"""
Created on 1 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.manager.byline.byline import Byline, DeviceBylineGroup, TopicBylineGroup
from scs_core.aws.manager.byline.byline_intercourse import BylineFinderResponse
from scs_core.aws.manager.byline.byline_manager import Endpoint


# --------------------------------------------------------------------------------------------------------------------

class BylineFinder(APIClient):
    """
    classdocs
    """

    DEVICE = 'device'
    TOPIC = 'topic'
    INCLUDE_MESSAGES = 'include-messages'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reporter=None):
        super().__init__(reporter=reporter)


    # ----------------------------------------------------------------------------------------------------------------

    def find_topics(self, token):
        params = {self.INCLUDE_MESSAGES: False}

        topics = set()
        for byline in self._get_blocks(Endpoint.url(), token, BylineFinderResponse, params=params):
            topics.add(byline.topic)

        return sorted(topics)


    def find_topics_for_device(self, token, device):
        params = {self.DEVICE: device, self.INCLUDE_MESSAGES: False}

        response = requests.get(Endpoint.url(), headers=self._token_headers(token), params=params)
        self._check_response(response)

        topics = set()
        for topic in [jdict.get('topic') for jdict in response.json()]:
            topics.add(topic)

        return sorted(topics)


    # ----------------------------------------------------------------------------------------------------------------

    def find_latest_byline_for_topic(self, token, topic, include_messages=True):
        params = {self.TOPIC: topic, self.INCLUDE_MESSAGES: include_messages}

        response = requests.get(Endpoint.url(), headers=self._token_headers(token), params=params)
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


    def find_bylines(self, token, excluded=None, strict_tags=False, include_messages=True):
        params = {self.INCLUDE_MESSAGES: include_messages}

        bylines = [item for item in self._get_blocks(Endpoint.url(), token, BylineFinderResponse, params=params)]

        return TopicBylineGroup.construct(bylines, excluded=excluded, strict_tags=strict_tags)


    def find_bylines_for_topic(self, token, topic, excluded=None, strict_tags=False, include_messages=True):
        params = {self.TOPIC: topic, self.INCLUDE_MESSAGES: include_messages}

        response = requests.get(Endpoint.url(), headers=self._token_headers(token), params=params)
        self._check_response(response)

        jdict = response.json()

        # bylines...
        return TopicBylineGroup.construct_from_jdict(jdict, excluded=excluded, strict_tags=strict_tags, skeleton=True)


    def find_bylines_for_device(self, token, device, excluded=None, include_messages=True):
        params = {self.DEVICE: device, self.INCLUDE_MESSAGES: include_messages}

        response = requests.get(Endpoint.url(), headers=self._token_headers(token), params=params)
        self._check_response(response)

        jdict = response.json()

        # bylines...
        return DeviceBylineGroup.construct_from_jdict(jdict, excluded=excluded, skeleton=True)


# --------------------------------------------------------------------------------------------------------------------

class DeviceBylineFinder(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find_byline_for_topic(self, token, topic, include_messages=True):
        url = Endpoint.url('self')
        params = {BylineFinder.INCLUDE_MESSAGES: include_messages}

        response = requests.get(url, headers=self._token_headers(token), params=params)
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
