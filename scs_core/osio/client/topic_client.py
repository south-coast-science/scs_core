"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class TopicClient(object):
    """
    classdocs
    """

    __HOST = "mqtt.opensensors.io"


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, message_client, auth):
        """
        Constructor
        """
        self.__message_client = message_client
        self.__message_client.connect(TopicClient.__HOST, auth.client_id, auth.user_id, auth.client_password)


    # ----------------------------------------------------------------------------------------------------------------

    def publish(self, topic, datum):
        datum_jstr = JSONify.dumps(datum)
        self.__message_client.publish(topic, datum_jstr)


    def subscribe(self, topic):
        for payload_jstr in self.__message_client.subscribe(topic):
            path_dict = PathDict.construct_from_jstr(payload_jstr)

            yield (path_dict)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
            return "TopicClient:{message_client:%s}" % self.__message_client
