"""
Created on 6 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DEPRECATED: this version of MessageManager for AWS EC2 server with single-part response.

https://xy1eszuu23.execute-api.us-west-2.amazonaws.com/staging/topicMessages?
topic=south-coast-science-dev/production-test/loc/1/gases&startTime=2018-03-31T10:45:50Z&endTime=2018-03-31T10:46:50Z
"""

from scs_core.aws.client.rest_client import RESTClient
from scs_core.aws.data.message import Message

from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class MessageManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__rest_client = RESTClient()


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_topic(self, topic, start_date, end_date):
        request_path = '/' + '/'.join((topic, start_date.utc().as_iso8601(), end_date.utc().as_iso8601()))

        # request...
        self.__rest_client.connect()

        try:
            jdict = self.__rest_client.get(request_path)

            # messages...
            collection = MessageResponse.construct_from_jdict(jdict)

            messages = [] if collection is None else collection.items

        finally:
            self.__rest_client.close()

        return messages


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageManager:{rest_client:%s}" % self.__rest_client


# --------------------------------------------------------------------------------------------------------------------

class MessageResponse(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        items = [Message.construct_from_jdict(msg_jdict) for msg_jdict in jdict.get('Items')]

        count = jdict.get('Count')
        scanned_count = jdict.get('ScannedCount')

        return MessageResponse(items, count, scanned_count)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items, count, scanned_count):
        """
        Constructor
        """
        self.__items = items                        # list of Message
        self.__count = count                        # int
        self.__scanned_count = scanned_count        # int


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def items(self):
        return self.__items


    @property
    def count(self):
        return self.__count


    @property
    def scanned_count(self):
        return self.__scanned_count


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageResponse:{items:%s, count:%s, scanned_count:%s}" % \
               (Str.collection(self.items), self.count, self.scanned_count)
