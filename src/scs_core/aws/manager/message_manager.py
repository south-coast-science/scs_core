"""
Created on 6 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://xy1eszuu23.execute-api.us-west-2.amazonaws.com/staging/topicMessages?
topic=south-coast-science-dev/production-test/loc/1/gases&startTime=2018-03-31T10:45:50Z&endTime=2018-03-31T10:46:50Z
"""

from scs_core.aws.client.rest_client import RESTClient
from scs_core.aws.data.message import MessageCollection


# --------------------------------------------------------------------------------------------------------------------

class MessageManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, api_key, verbose=False):
        """
        Constructor
        """
        self.__rest_client = RESTClient(http_client, api_key)
        self.__verbose = verbose


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_topic(self, topic, start_date, end_date):
        request_path = '/staging/topicMessages'
        params = {'topic': topic, 'startTime': start_date.utc().as_iso8601(), 'endTime': end_date.utc().as_iso8601()}

        # request...
        self.__rest_client.connect()

        try:
            jdict = self.__rest_client.get(request_path, params)

            # messages...
            collection = MessageCollection.construct_from_jdict(jdict)

            messages = collection.items
        finally:
            self.__rest_client.close()

        return messages


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageManager:{rest_client:%s, verbose:%s}" % (self.__rest_client, self.__verbose)
