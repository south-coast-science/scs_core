"""
Created on 13 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

south-coast-science-dev
43308b72-ad41-4555-b075-b4245c1971db
"""

import urllib.parse

from scs_core.osio.client.rest_client import RESTClient
from scs_core.osio.data.topic import Topic


# --------------------------------------------------------------------------------------------------------------------

class TopicManager(object):
    """
    classdocs
    """
    __FINDER_BATCH_SIZE = 100

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, api_key):
        """
        Constructor
        """
        self.__rest_client = RESTClient(http_client, api_key)


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, topic_path):
        path = '/v1/topics' + urllib.parse.quote(topic_path, '')

        # request...
        self.__rest_client.connect()

        try:
            response_jdict = self.__rest_client.get(path)
        except RuntimeError:
            response_jdict = None

        self.__rest_client.close()

        topic = Topic.construct_from_jdict(response_jdict)

        return topic


    def find_for_org(self, org_id):
        offset = 0
        topics = []

        self.__rest_client.connect()

        try:
            while True:
                batch = self.__get(org_id, offset, self.__FINDER_BATCH_SIZE)

                if len(batch) == 0:
                    break

                topics.extend(batch)
                offset += len(batch)

        finally:
            self.__rest_client.close()

        return topics


    def create(self, topic):
        path = '/v2/topics'

        # request...
        self.__rest_client.connect()

        try:
            response = self.__rest_client.post(path, topic.as_json())

        finally:
            self.__rest_client.close()

        success = response == topic.path

        return success


    def delete(self, topic_path):
        path = '/v1/topics/' + urllib.parse.quote(topic_path, '')

        # request...
        self.__rest_client.connect()

        try:
            response = self.__rest_client.delete(path)

        finally:
            self.__rest_client.close()

        success = response == ''

        return success


    # ----------------------------------------------------------------------------------------------------------------

    def __get(self, org_id, offset, count):
        path = '/v2/org/' + org_id + '/topics'
        params = {'offset': offset, 'count': count}

        # request...
        response_jdict = self.__rest_client.get(path, params)

        topics_jdict = response_jdict.get('topics')
        topics = [Topic.construct_from_jdict(topic_jdict) for topic_jdict in topics_jdict] if topics_jdict else []

        return topics


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicManager:{rest_client:%s}" % self.__rest_client
