"""
Created on 8 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"tag": "scs-be2-2", "shared-secret": "secret1",
"topic": "south-coast-science-dev/production-test/device/alpha-bb-eng-000002/control"}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MQTTPeer(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        tag = jdict.get('tag')
        shared_secret = jdict.get('shared-secret')
        topic = jdict.get('topic')

        return MQTTPeer(tag, shared_secret, topic)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, shared_secret, topic):
        """
        Constructor
        """
        self.__tag = tag                                        # string
        self.__shared_secret = shared_secret                    # string
        self.__topic = topic                                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['shared-secret'] = self.shared_secret
        jdict['topic'] = self.topic

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def shared_secret(self):
        return self.__shared_secret


    @shared_secret.setter
    def shared_secret(self, shared_secret):
        self.__shared_secret = shared_secret


    @property
    def topic(self):
        return self.__topic


    @topic.setter
    def topic(self, topic):
        self.__topic = topic


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTPeer:{tag:%s, shared_secret:%s, topic:%s}" % \
               (self.tag, self.shared_secret, self.topic)
