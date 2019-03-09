"""
Created on 8 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"devices": {"scs-ap1-6": {"tag": "scs-ap1-6", "shared-secret": "secret",
"topic": "south-coast-science-dev/development/device/alpha-pi-eng-000006/control"}}
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
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        devices = OrderedDict()

        for item in jdict.get('devices').values():
            access = ControlAccess.construct_from_jdict(item)

            devices[access.tag] = access

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
        self.__devices[device.tag] = device

        # sort...
        devices = OrderedDict()

        for key in sorted(self.__devices.keys()):
            devices[key] = self.__devices[key]

        self.__devices = devices


    def remove(self, tag):
        del(self.__devices[tag])


    def device(self, tag):
        try:
            return self.__devices[tag]

        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def devices(self):
        return self.__devices.values()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        devices = '[' + ', '.join([tag + ': ' + str(access) for tag, access in self.__devices.items()]) + ']'

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

        tag = jdict.get('tag')
        shared_secret = jdict.get('shared-secret')
        topic = jdict.get('topic')

        return ControlAccess(tag, shared_secret, topic)


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


    @property
    def topic(self):
        return self.__topic


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ControlAccess:{tag:%s, shared_secret:%s, topic:%s}" % (self.tag, self.shared_secret, self.topic)
