"""
Created on 8 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"peers": {"scs-bbe-002": {"hostname": "scs-bbe-002", "tag": "scs-be2-2", "shared-secret": "secret1",
"topic": "south-coast-science-dev/production-test/device/alpha-bb-eng-000002/control"}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable, PersistentJSONable
from scs_core.data.str import Str


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

        hostname = jdict.get('hostname')
        tag = jdict.get('tag')
        shared_secret = jdict.get('shared-secret')
        topic = jdict.get('topic')

        return MQTTPeer(hostname, tag, shared_secret, topic)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, hostname, tag, shared_secret, topic):
        """
        Constructor
        """
        self.__hostname = hostname                              # string
        self.__tag = tag                                        # string
        self.__shared_secret = shared_secret                    # string
        self.__topic = topic                                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['hostname'] = self.hostname
        jdict['tag'] = self.tag
        jdict['shared-secret'] = self.shared_secret
        jdict['topic'] = self.topic

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def hostname(self):
        return self.__hostname


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
        return "MQTTPeer:{hostname:%s, tag:%s, shared_secret:%s, topic:%s}" % \
               (self.hostname, self.tag, self.shared_secret, self.topic)


# --------------------------------------------------------------------------------------------------------------------

class MQTTPeerSet(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME =    "mqtt_peers.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    @classmethod
    def load(cls, manager, encryption_key=None, skeleton=False):
        instance = super().load(manager, encryption_key=encryption_key, skeleton=skeleton)

        if instance is None:
            instance = cls(OrderedDict())

        return instance


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        peers = OrderedDict()

        for hostname, item in jdict.get('peers').items():
            peer = MQTTPeer.construct_from_jdict(item)

            peers[hostname] = peer

        return cls(peers)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, peers):
        """
        Constructor
        """
        super().__init__()

        self.__peers = peers                                # OrderedDict of string: MQTTPeer


    def __len__(self):
        return len(self.__peers)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['peers'] = self.__peers

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def insert(self, peer: MQTTPeer):
        # add...
        self.__peers[peer.hostname] = peer

        # sort...
        peers = OrderedDict()

        for hostname in sorted(self.__peers.keys()):
            peers[hostname] = self.__peers[hostname]

        self.__peers = peers


    def remove(self, hostname):
        try:
            del(self.__peers[hostname])
            return True

        except KeyError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def subset(self, hostname_substring=None, topic_substring=None):
        subset = OrderedDict()

        for hostname, peer in self.__peers.items():
            if hostname_substring is not None and hostname_substring not in hostname:
                continue

            if topic_substring is not None and topic_substring not in peer.topic:
                continue

            subset[peer.hostname] = peer

        return MQTTPeerSet(subset)


    def peer(self, hostname):
        try:
            return self.__peers[hostname]
        except KeyError:
            return None


    def peer_by_tag(self, tag):
        for peer in self.__peers.values():
            if peer.tag == tag:
                return peer

        return None


    @property
    def peers(self):
        return list(self.__peers.values())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTPeerSet:{peers:%s}" % Str.collection(self.__peers)
