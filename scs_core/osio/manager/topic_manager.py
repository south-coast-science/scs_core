"""
Created on 13 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import urllib.parse

from scs_core.osio.client.rest_client import RESTClient
from scs_core.osio.data.topic_summary import TopicSummary
from scs_core.osio.data.topic_metadata import TopicMetadata


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
        if topic_path is None:
            return None

        request_path = '/v1/topics/' + urllib.parse.quote(topic_path, '')

        # request...
        self.__rest_client.connect()

        try:
            response_jdict = self.__rest_client.get(request_path)
        except RuntimeError:
            response_jdict = None

        self.__rest_client.close()

        topic = TopicMetadata.construct_from_jdict(response_jdict)

        return topic


    def find_for_org(self, org_id, partial_topic_path=None, topic_schema=None):
        topics = []

        # request...
        self.__rest_client.connect()

        try:
            for batch in self.__find(org_id, partial_topic_path, topic_schema):
                topics.extend(batch)

        finally:
            self.__rest_client.close()

        return topics


    # ----------------------------------------------------------------------------------------------------------------

    def __find(self, org_id, partial_topic_path=None, topic_schema=None):
        request_path = '/v2/orgs/' + org_id + '/topics'
        params = {'offset': 0, 'count': self.__FINDER_BATCH_SIZE}

        while True:
            # request...
            response_jdict = self.__rest_client.get(request_path, params)

            # topics...
            topics_jdict = response_jdict.get('topics')

            topics = []

            if topics_jdict:
                for topic_jdict in topics_jdict:
                    topic = TopicSummary.construct_from_jdict(topic_jdict)

                    if partial_topic_path is not None and partial_topic_path not in topic.path:
                        continue

                    if topic_schema is not None and (topic.schema_id != topic_schema):
                        continue

                    topics.append(topic)

            yield topics

            if len(topics_jdict) == 0:
                break

            # next...
            params['offset'] += len(topics_jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, topic):
        request_path = '/v2/topics'

        # request...
        self.__rest_client.connect()

        try:
            response = self.__rest_client.post(request_path, topic.as_json())

        finally:
            self.__rest_client.close()

        success = response == topic.path

        return success


    def update(self, topic_path, topic):
        request_path = '/v1/topics/' + topic_path

        # request...
        self.__rest_client.connect()

        try:
            self.__rest_client.put(request_path, topic.as_json())
        finally:
            self.__rest_client.close()


    def delete(self, topic_path):
        request_path = '/v1/topics/' + urllib.parse.quote(topic_path, '')

        # request...
        self.__rest_client.connect()

        try:
            response = self.__rest_client.delete(request_path)

        finally:
            self.__rest_client.close()

        success = response == ''

        return success


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicManager:{rest_client:%s}" % self.__rest_client
