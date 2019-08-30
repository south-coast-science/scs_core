"""
Created on 26 Aug 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from enum import Enum

from scs_core.data.json import JSONReport


# --------------------------------------------------------------------------------------------------------------------

class QueueReport(JSONReport):
    """
    classdocs
   """
    __BACKLOG_MIN =             4           # documents

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return QueueReport(0, ClientStatus.DISCONNECTED, False)

        length = jdict.get('length')
        client_state = ClientStatus(jdict.get('client-state'))
        publish_success = jdict.get('publish-success')

        return QueueReport(length, client_state, publish_success)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, length, client_state, publish_success):
        """
        Constructor
        """
        self.__length = length                                  # int or None
        self.__client_state = client_state                      # int
        self.__publish_success = publish_success                # bool


    # ----------------------------------------------------------------------------------------------------------------

    def has_backlog(self):
        return self.__length is not None and self.__length > self.__BACKLOG_MIN


    def status(self):
        # client INHIBITED...
        if self.client_state == ClientStatus.INHIBITED:
            return QueueStatus.INHIBITED

        # client DISCONNECTED...
        if self.client_state == ClientStatus.DISCONNECTED:
            return QueueStatus.DISCONNECTED

        # any client state...
        if not self.has_backlog() and self.publish_success:
            return QueueStatus.PUBLISHING

        if self.has_backlog() and self.publish_success:
            return QueueStatus.CLEARING

        if not self.publish_success:
            return QueueStatus.QUEUING

        # unknown / error...
        return QueueStatus.NONE


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['length'] = self.length
        jdict['client-state'] = self.client_state.name
        jdict['publish-success'] = self.publish_success

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def length(self):
        return self.__length


    @length.setter
    def length(self, length):
        self.__length = length


    @property
    def client_state(self):
        return self.__client_state


    @client_state.setter
    def client_state(self, client_state):
        self.__client_state = client_state


    @property
    def publish_success(self):
        return self.__publish_success


    @publish_success.setter
    def publish_success(self, publish_success):
        self.__publish_success = publish_success


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "QueueReport:{length:%s, client_state:%s, publish_success:%s}" % \
               (self.length, self.client_state, self.publish_success)


# --------------------------------------------------------------------------------------------------------------------

class ClientStatus(Enum):
    """
    classdocs
   """
    INHIBITED =         1
    DISCONNECTED =      2
    CONNECTED =         3


# --------------------------------------------------------------------------------------------------------------------

class QueueStatus(Enum):
    """
    classdocs
   """
    NONE =              1
    INHIBITED =         2
    DISCONNECTED =      3
    PUBLISHING =        4
    QUEUING =           5
    CLEARING =          6
