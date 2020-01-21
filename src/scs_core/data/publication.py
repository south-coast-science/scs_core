"""
Created on 22 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Publication(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        topic = jdict.get('topic')
        priority = jdict.get('priority')
        payload = jdict.get('payload')

        return Publication(topic, priority, payload)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, priority, payload):
        """
        Constructor
        """
        self.__topic = topic                        # string
        self.__priority = int(priority)             # int
        self.__payload = payload                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['topic'] = self.topic
        jdict['priority'] = self.priority
        jdict['payload'] = self.payload

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def priority(self):
        return self.__priority


    @property
    def payload(self):
        return self.__payload


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Publication:{topic:%s, priority:%s, payload:%s}" % (self.topic, self.priority, self.payload)
