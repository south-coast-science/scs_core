"""
Created on 20 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
event: message
data: {"topic":"/users/southcoastscience-dev/test/json","date":1479655521714,
"message":"{\"rec\": \"2016-11-20T15:25:29.605+00:00\", \"val\": {\"host\": {\"tmp\": 46.2}}}"}
"""

import datetime

from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class MessageEvent(object):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        topic = jdict.get('topic')
        date = datetime.datetime.fromtimestamp(jdict.get('date') / 1e3)         # Warning: JavaScript timestamp!
        message_jstr = jdict.get('message')

        message_jdict = PathDict.construct_from_jstr(message_jstr)

        return MessageEvent(topic, date, message_jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, date, message):
        """
        Constructor
        """
        self.__topic = topic            # string
        self.__date = date              # datetime

        self.__message = message        # PathDict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def date(self):
        return self.__date


    @property
    def message(self):
        return self.__message


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageEvent:{topic:%s, date:%s, message:%s}" % (self.topic, self.date, self.message)
