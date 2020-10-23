"""
Created on 25 Dec 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Equivalent to cURLs:
curl "https://aws.southcoastscience.com/device-topics?topic=south-coast-science-dev/alphasense/loc/303/gases"
curl "https://aws.southcoastscience.com/device-topics?device=scs-bgx-303"
"""

from scs_core.aws.client.rest_client import RESTClient
from scs_core.aws.data.byline import Byline, DeviceBylineGroup, TopicBylineGroup


# --------------------------------------------------------------------------------------------------------------------

class BylineManager(object):
    """
    classdocs
    """

    __DEVICE =      'device'
    __TOPIC =       'topic'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, api_key):
        """
        Constructor
        """
        self.__rest_client = RESTClient(api_key)


    # ----------------------------------------------------------------------------------------------------------------

    def find_latest_byline_for_topic(self, topic):
        request_path = '/device-topics'

        params = {self.__TOPIC: topic}

        # request...
        self.__rest_client.connect()

        try:
            jdict = self.__rest_client.get(request_path, params)

            # bylines...
            if jdict is None:
                return None

            latest_byline = None

            for item in jdict:
                byline = Byline.construct_from_jdict(item)

                if latest_byline is None or latest_byline.rec < byline.rec:
                    latest_byline = byline

            return latest_byline

        finally:
            self.__rest_client.close()


    def find_bylines_for_topic(self, topic, excluded=None):
        request_path = '/device-topics'

        params = {self.__TOPIC: topic}

        # request...
        self.__rest_client.connect()

        try:
            jdict = self.__rest_client.get(request_path, params)

            # bylines...
            return TopicBylineGroup.construct_from_jdict(jdict, excluded=excluded)

        finally:
            self.__rest_client.close()


    def find_bylines_for_device(self, device, excluded=None):
        request_path = '/device-topics'

        params = {self.__DEVICE: device}

        # request...
        self.__rest_client.connect()

        try:
            jdict = self.__rest_client.get(request_path, params)

            # bylines...
            return DeviceBylineGroup.construct_from_jdict(jdict, excluded=excluded)

        finally:
            self.__rest_client.close()


    def find_byline_for_device_topic(self, device, topic):
        request_path = '/device-topics'

        params = {self.__DEVICE: device}

        # request...
        self.__rest_client.connect()

        try:
            jdict = self.__rest_client.get(request_path, params)

            # bylines...
            if jdict is None:
                return None

            for item in jdict:
                byline = Byline.construct_from_jdict(item)

                if byline.topic == topic:
                    return byline

            return None

        finally:
            self.__rest_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BylineManager:{rest_client:%s}" % self.__rest_client
