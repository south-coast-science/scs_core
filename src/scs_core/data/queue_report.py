"""
Created on 26 Aug 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONReport


# --------------------------------------------------------------------------------------------------------------------

class QueueReport(JSONReport):
    """
    classdocs
   """
    CLIENT_INHIBITED =          11
    CLIENT_DISCONNECTED =       12
    CLIENT_CONNECTED =          13

    STATUS_NONE =               21
    STATUS_INHIBITED =          22
    STATUS_DISCONNECTED =       23
    STATUS_PUBLISHING =         24
    STATUS_QUEUING =            25
    STATUS_CLEARING =           26

    __BACKLOG_MIN =             4           # documents


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return QueueReport(0, cls.CLIENT_DISCONNECTED, False)

        length = jdict.get('length')
        client_state = jdict.get('client-state')
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
        if self.client_state == self.CLIENT_INHIBITED:
            return self.STATUS_INHIBITED

        if self.client_state == self.CLIENT_DISCONNECTED:
            return self.STATUS_DISCONNECTED

        if not self.has_backlog() and self.publish_success:
            return self.STATUS_PUBLISHING

        if self.has_backlog() and self.publish_success:
            return self.STATUS_CLEARING

        if self.has_backlog() and not self.publish_success:
            return self.STATUS_QUEUING

        return self.STATUS_NONE


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['length'] = self.length
        jdict['client-state'] = self.client_state
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
