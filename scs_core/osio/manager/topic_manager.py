"""
Created on 13 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
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
        path = '/v1/topics/' + urllib.parse.quote(topic_path, '')

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
        topics = []

        # request...
        self.__rest_client.connect()

        try:
            for batch in self.__get(org_id):
                topics.extend(batch)

        finally:
            self.__rest_client.close()

        return topics


    # ----------------------------------------------------------------------------------------------------------------

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


    def update(self, topic):
        pass                    # TODO: implement update(..)


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

    def __get(self, org_id):
        path = '/v2/orgs/' + org_id + '/topics'
        params = {'offset': 0, 'count': self.__FINDER_BATCH_SIZE}

        while True:
            # request...
            response_jdict = self.__rest_client.get(path, params)

            # topics...
            topics_jdict = response_jdict.get('topics')
            topics = [Topic.construct_from_jdict(topic_jdict) for topic_jdict in topics_jdict] if topics_jdict else []

            yield topics

            if len(topics) == 0:
                break

            # next...
            params['offset'] = len(topics)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicManager:{rest_client:%s}" % self.__rest_client
