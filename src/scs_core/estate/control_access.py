"""
Created on 8 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"devices": {"scs-bbe-002": {"hostname": "scs-bbe-002", "tag": "scs-be2-2", "shared-secret": "secret1",
"topic": "south-coast-science-dev/production-test/device/alpha-bb-eng-000002/control"}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable, PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class ControlAccessSet(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME =    "control_access.json"

    @classmethod
    def persistence_location(cls, hostname):
        return hostname.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        devices = OrderedDict()

        for hostname, item in jdict.get('devices').items():
            device = ControlAccess.construct_from_jdict(item)

            devices[hostname] = device

        return ControlAccessSet(devices)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, devices):
        """
        Constructor
        """
        super().__init__()

        self.__devices = devices                                # dictionary of string: ControlAccess


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['devices'] = self.__devices

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def insert(self, device):
        # add...
        self.__devices[device.hostname] = device

        # sort...
        devices = OrderedDict()

        for hostname in sorted(self.__devices.keys()):
            devices[hostname] = self.__devices[hostname]

        self.__devices = devices


    def remove(self, hostname):
        del(self.__devices[hostname])


    # ----------------------------------------------------------------------------------------------------------------

    def device(self, hostname):
        try:
            return self.__devices[hostname]

        except KeyError:
            return None


    @property
    def devices(self):
        return self.__devices.values()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        devices = '{' + ', '.join([hostname + ': ' + str(device) for hostname, device in self.__devices.items()]) + '}'

        return "ControlAccessSet:{devices:%s}" % devices


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

        hostname = jdict.get('hostname')
        tag = jdict.get('tag')
        shared_secret = jdict.get('shared-secret')
        topic = jdict.get('topic')

        return ControlAccess(hostname, tag, shared_secret, topic)


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
        return "ControlAccess:{hostname:%s, tag:%s, shared_secret:%s, topic:%s}" % \
               (self.hostname, self.tag, self.shared_secret, self.topic)
