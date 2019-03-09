"""
Created on 8 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"auths": {"scs-bbe-002": {"hostname": "scs-bbe-002", "tag": "scs-be2-2", "shared-secret": "secret1",
"topic": "south-coast-science-dev/production-test/device/alpha-bb-eng-000002/control"}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable, PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class MQTTControlAuthSet(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME =    "mqtt_control_auths.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        auths = OrderedDict()

        for hostname, item in jdict.get('auths').items():
            auth = MQTTControlAuth.construct_from_jdict(item)

            auths[hostname] = auth

        return MQTTControlAuthSet(auths)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, auths):
        """
        Constructor
        """
        super().__init__()

        self.__auths = auths                                # dictionary of string: MQTTControlAuth


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['auths'] = self.__auths

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def insert(self, auth):
        # add...
        self.__auths[auth.hostname] = auth

        # sort...
        auths = OrderedDict()

        for hostname in sorted(self.__auths.keys()):
            auths[hostname] = self.__auths[hostname]

        self.__auths = auths


    def remove(self, hostname):
        try:
            del(self.__auths[hostname])

        except KeyError:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def auth(self, hostname):
        try:
            return self.__auths[hostname]

        except KeyError:
            return None


    @property
    def auths(self):
        return self.__auths.values()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        auths = '{' + ', '.join([hostname + ': ' + str(auth) for hostname, auth in self.__auths.items()]) + '}'

        return "MQTTControlAuthSet:{auths:%s}" % auths


# --------------------------------------------------------------------------------------------------------------------

class MQTTControlAuth(JSONable):
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

        return MQTTControlAuth(hostname, tag, shared_secret, topic)


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


    @property
    def topic(self):
        return self.__topic


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTControlAuth:{hostname:%s, tag:%s, shared_secret:%s, topic:%s}" % \
               (self.hostname, self.tag, self.shared_secret, self.topic)
