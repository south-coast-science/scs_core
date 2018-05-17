"""
Created on 17 May 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

settings for OPCMonitor

example JSON:
{"inhibit-publishing": false}
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class MQTTConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "mqtt_conf.json"

    @classmethod
    def filename(cls, host):
        return os.path.join(host.conf_dir(), cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return MQTTConf(False)

        inhibit_publishing = jdict.get('inhibit-publishing')

        return MQTTConf(inhibit_publishing)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, inhibit_publishing):
        """
        Constructor
        """
        super().__init__()

        self.__inhibit_publishing = bool(inhibit_publishing)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def inhibit_publishing(self):
        return self.__inhibit_publishing


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['inhibit-publishing'] = self.inhibit_publishing

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTConf:{inhibit_publishing:%s}" %  self.inhibit_publishing
