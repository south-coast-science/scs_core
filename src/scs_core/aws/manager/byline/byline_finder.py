"""
Created on 1 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Equivalent to cURLs:
curl "https://aws.southcoastscience.com/device-topics?topic=south-coast-science-dev/alphasense/loc/303/gases"
curl "https://aws.southcoastscience.com/device-topics?device=scs-bgx-303"
"""

import requests

from scs_core.aws.client.api_client import APIClient

from scs_core.aws.manager.byline.byline import Byline, DeviceBylineGroup, TopicBylineGroup
from scs_core.aws.manager.byline.byline_intercourse import BylineFinderResponse


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
