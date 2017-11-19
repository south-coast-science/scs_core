"""
Created on 6 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import urllib.parse

from scs_core.aws.client.rest_client import RESTClient
from scs_core.aws.data.message import Message


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
        request_path = '/v1/messages/topic/' + urllib.parse.quote(topic, safe='')
        params = {'start-date': start_date.as_iso8601(), 'end-date': end_date.as_iso8601()}

        # request...
        self.__rest_client.connect()

        try:
            jdict = self.__rest_client.get(request_path, params)

            # messages...
            messages = [Message.construct_from_jdict(msg_jdict) for msg_jdict in jdict] if jdict else []
        finally:
            self.__rest_client.close()

        return messages


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageManager:{rest_client:%s, verbose:%s}" % (self.__rest_client, self.__verbose)
