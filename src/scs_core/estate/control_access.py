"""
Created on 8 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"tag": 788, "shared_secret": "Tunisia", "topic": "TUN"}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable, PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class ControlAccessSet(PersistentJSONable):
    """
    classdocs
    """

    @classmethod
    def persistence_location(cls, _):
        raise NotImplementedError


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        accesses = {}

        for item in jdict.get('accesses').items():
            access = ControlAccess.construct_from_jdict(item)

            accesses[access.tag] = access

        return ControlAccessSet(accesses)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, accesses):
        """
        Constructor
        """
        super().__init__()

        self.__accesses = accesses                              # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['accesses'] = self.accesses

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def accesses(self):
        return self.__accesses


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        accesses = '[' + ','.join([access.tag + ': ' + access for access in self.accesses.items])

        return "ControlAccessSet:{accesses:%s}" % accesses


# --------------------------------------------------------------------------------------------------------------------

class ControlAccess(JSONable):
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

        return ControlAccess(tag, shared_secret, topic)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, shared_secret, topic):
        """
        Constructor
        """
        self.__tag = tag                                    # string
        self.__shared_secret = shared_secret                # string
        self.__topic = topic                                # string


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


    @property
    def topic(self):
        return self.__topic


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ControlAccess:{tag:%s, shared_secret:%s, topic:%s}" % (self.tag, self.shared_secret, self.topic)
