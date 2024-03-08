"""
Created on 1 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.aws_endpoint import AWSEndpoint
from scs_core.aws.manager.byline.byline import Byline, DeviceBylineGroup, TopicBylineGroup
from scs_core.aws.manager.byline.byline_intercourse import BylineFinderResponse


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(AWSEndpoint):
    @classmethod
    def configuration(cls):
        return cls('BylineAPI/TopicBylines',
                   'https://k5uz49605m.execute-api.us-west-2.amazonaws.com/default/TopicBylines')


# --------------------------------------------------------------------------------------------------------------------

class BylineFinder(APIClient):
    """
    classdocs
    """

    __DEVICE = 'device'
    __TOPIC = 'topic'
    __EXCLUDE_MESSAGES = 'exclude-messages'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reporter=None):
        super().__init__(reporter=reporter)


    # ----------------------------------------------------------------------------------------------------------------

    def find_latest_byline_for_topic(self, token, topic, exclude_messages=False):
        params = {self.__TOPIC: topic, self.__EXCLUDE_MESSAGES: exclude_messages}

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


    def find_bylines(self, token, excluded=None, strict_tags=False, exclude_messages=False):
        params = {self.__EXCLUDE_MESSAGES: exclude_messages}

        bylines = [item for item in self._get_blocks(Endpoint.url(), token, BylineFinderResponse, params=params)]

        return TopicBylineGroup.construct(bylines, excluded=excluded, strict_tags=strict_tags)


    def find_bylines_for_topic(self, token, topic, excluded=None, strict_tags=False, exclude_messages=False):
        params = {self.__TOPIC: topic, self.__EXCLUDE_MESSAGES: exclude_messages}

        response = requests.get(Endpoint.url(), headers=self._token_headers(token), params=params)
        self._check_response(response)

        jdict = response.json()

        # bylines...
        return TopicBylineGroup.construct_from_jdict(jdict, excluded=excluded, strict_tags=strict_tags, skeleton=True)


    def find_bylines_for_device(self, token, device, excluded=None, exclude_messages=False):
        params = {self.__DEVICE: device, self.__EXCLUDE_MESSAGES: exclude_messages}

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

    def find_byline_for_topic(self, token, topic):
        url = Endpoint.url('self')

        response = requests.get(url, headers=self._token_headers(token))
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
