"""
Created on 13 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

deliver-change
870725f3-e692-4538-aa81-bfa8b51d44e7

south-coast-science-dev
43308b72-ad41-4555-b075-b4245c1971db
"""

from scs_core.osio.client.rest_client import RESTClient
from scs_core.osio.data.topic import Topic


# --------------------------------------------------------------------------------------------------------------------

class TopicManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, api_key):
        """
        Constructor
        """
        self.__rest_client = RESTClient(http_client, api_key)


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_org(self, org_id):
        path = '/v2/orgs/' + org_id + '/topics'

        # request...
        self.__rest_client.connect()

        response_jdict = self.__rest_client.get(path)

        self.__rest_client.close()

        topics_jdict = response_jdict.get('topics')
        topics = [Topic.construct_from_jdict(topic_jdict) for topic_jdict in topics_jdict] if topics_jdict else []

        return topics


    def create(self, topic):
        path = '/v2/topics'

        # request...
        self.__rest_client.connect()

        response = self.__rest_client.post(path, topic.as_json())

        self.__rest_client.close()

        success = response == topic.path        # TODO: handle error document otherwise

        return success


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicManager:{rest_client:%s}" % self.__rest_client
