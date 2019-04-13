"""
Created on 20 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import re


# --------------------------------------------------------------------------------------------------------------------

class RealtimeClient(object):
    """
    classdocs
    """

    __HOST = "realtime.opensensors.io"          # hard-coded URL


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, streaming_client, listener, auth):
        """
        Constructor
        """
        self.__streaming_client = streaming_client
        self.__listener = listener
        self.__auth = auth


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self, topic):
        path = "/v1/public/events/topics/" + topic
        payload = {"token": self.__auth.api_key}

        self.__streaming_client.connect(self.__local_listener, RealtimeClient.__HOST, path, payload)


    def close(self):
        self.__streaming_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __local_listener(self, message):
        matches = re.search(r'data:\s*(.+)', message)

        if not matches:
            return

        datum = matches.group(1)
        self.__listener(datum)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "RealtimeClient:{streaming_client:%s, auth:%s}" % (self.__streaming_client, self.__auth)
