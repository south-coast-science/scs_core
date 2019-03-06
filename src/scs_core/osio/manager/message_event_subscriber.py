"""
Created on 20 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
event: message
data: {"topic":"/users/southcoastscience-dev/test/json","date":1479655521714,
            "message":"{\"rec\": \"2016-11-20T15:25:29.605+00:00\", \"val\": {\"host\": {\"tmp\": 46.2}}}"}
"""

import json

from scs_core.osio.client.realtime_client import RealtimeClient
from scs_core.osio.data.message_event import MessageEvent


# --------------------------------------------------------------------------------------------------------------------

class MessageEventSubscriber(object):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, streaming_client):
        self.__streaming_client = streaming_client

        self.__listener = None
        self.__realtime_client = None


    # ----------------------------------------------------------------------------------------------------------------

    def subscribe(self, listener, auth, topic):
        self.close()

        self.__listener = listener

        self.__realtime_client = RealtimeClient(self.__streaming_client, self.__local_listener, auth)
        self.__realtime_client.connect(topic)


    def close(self):                        # TODO: sort out order of closing
        if not self.__realtime_client:
            return

        self.__realtime_client.close()
        self.__realtime_client = None


    # ----------------------------------------------------------------------------------------------------------------

    def __local_listener(self, datum):
        if not self.__listener:
            return

        jdict = json.loads(datum)
        event = MessageEvent.construct_from_jdict(jdict)

        self.__listener(event)


# ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageEventSubscriber:{streaming_client:%s}" % self.__streaming_client
