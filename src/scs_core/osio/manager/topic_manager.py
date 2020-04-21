"""
Created on 13 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import socket

import urllib.parse

from collections import OrderedDict

from scs_core.osio.client.rest_client import RESTClient

from scs_core.osio.data.device_topic import DeviceTopic
from scs_core.osio.data.topic_summary import TopicSummary
from scs_core.osio.data.topic_metadata import TopicMetadata
from scs_core.osio.data.user_topic import UserTopic

from scs_core.osio.manager.message_manager import NextMessageQuery


# --------------------------------------------------------------------------------------------------------------------

class TopicManager(object):
    """
    classdocs
    """
    __FINDER_BATCH_SIZE = 100

    __TIMEOUT = 10.0                            # Required because of OSIO non-response on CRUD operations.


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


    def find_for_user(self, user_id):
        topics = []

        # request...
        self.__rest_client.connect()

        try:
            for batch in self.__find_for_user(user_id):
                topics.extend(batch)

        finally:
            self.__rest_client.close()

        return topics


    def find_for_device(self, client_id, start_date, end_date):
        request_path = '/v1/messages/device/' + client_id
        params = {'start-date': start_date.as_iso8601(), 'end-date': end_date.as_iso8601()}

        topics = {}

        # request...
        self.__rest_client.connect()

        try:
            while True:
                jdict = self.__rest_client.get(request_path, params)

                # messages...
                for message in jdict['messages']:
                    if message['topic'] not in topics:
                        topics[message['topic']] = DeviceTopic.construct_from_message_jdict(message)

                # next...
                next_query = NextMessageQuery.construct_from_uri(jdict.get('next'))

                if next_query is None:
                    break

                params['start-date'] = next_query.start_date.as_iso8601()
                params['end-date'] = next_query.end_date.as_iso8601()

            sorted_topics = OrderedDict(sorted(topics.items()))

            return list(sorted_topics.values())

        finally:
            self.__rest_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __find(self, org_id, partial_topic_path=None, topic_schema=None):
        request_path = '/v2/orgs/' + org_id + '/topics'
        params = {'offset': 0, 'count': self.__FINDER_BATCH_SIZE}

        while True:
            topics = []

            # request...
            response_jdict = self.__rest_client.get(request_path, params)

            if response_jdict is None:
                return

            # topics...
            topics_jdict = response_jdict.get('topics')

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
                return

            # next...
            params['offset'] += len(topics_jdict)


    def __find_for_user(self, user_id):
        request_path = '/v1/users/' + user_id + '/topics'
        params = {'offset': 0, 'count': self.__FINDER_BATCH_SIZE}

        while True:
            # request...
            topics_jdict = self.__rest_client.get(request_path, params)

            # topics...
            topics = [UserTopic.construct_from_jdict(topic_jdict) for topic_jdict in topics_jdict]

            yield topics

            if len(topics_jdict) == 0:
                return

            # next...
            params['offset'] += len(topics_jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, topic):
        request_path = '/v2/topics'

        # request...
        self.__rest_client.connect(timeout=self.__TIMEOUT)

        try:
            response = self.__rest_client.post(request_path, topic.as_json())

        except socket.timeout:
            return True

        finally:
            self.__rest_client.close()

        success = response == topic.path

        return success


    def update(self, topic_path, topic):
        request_path = '/v1/topics/' + topic_path

        # request...
        self.__rest_client.connect(timeout=self.__TIMEOUT)

        try:
            self.__rest_client.put(request_path, topic.as_json())

        except socket.timeout:
            pass

        finally:
            self.__rest_client.close()


    def delete(self, topic_path):
        request_path = '/v1/topics/' + urllib.parse.quote(topic_path, '')

        # request...
        self.__rest_client.connect(timeout=self.__TIMEOUT)

        try:
            response = self.__rest_client.delete(request_path)

        except socket.timeout:
            return True

        finally:
            self.__rest_client.close()

        success = response == ''

        return success


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicManager:{rest_client:%s}" % self.__rest_client
