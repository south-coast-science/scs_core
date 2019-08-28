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

    __BACKLOG_MIN = 4

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        length = jdict.get('length')
        publish_success = jdict.get('publish-success')

        return QueueReport(length, publish_success)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, length, publish_success):
        """
        Constructor
        """
        self.__length = length                                  # int or None
        self.__publish_success = publish_success                # bool


    # ----------------------------------------------------------------------------------------------------------------

    def has_backlog(self):
        return self.__length is not None and self.__length > self.__BACKLOG_MIN


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['length'] = self.length
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
    def publish_success(self):
        return self.__publish_success


    @publish_success.setter
    def publish_success(self, publish_success):
        self.__publish_success = publish_success


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "QueueReport:{length:%s, publish_success:%s}" % (self.length, self.publish_success)
