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

    DEFAULT_QUEUE_SIZE = 21000              # 14 messages per minute * 60 * 24 = 20,160


    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "mqtt_conf.json"

    @classmethod
    def filename(cls, host):
        return os.path.join(host.conf_dir(), cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return MQTTConf(False, cls.DEFAULT_QUEUE_SIZE)

        inhibit_publishing = jdict.get('inhibit-publishing')
        queue_size = jdict.get('queue-size')

        if queue_size is None:
            queue_size = cls.DEFAULT_QUEUE_SIZE

        return MQTTConf(inhibit_publishing, queue_size)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, inhibit_publishing, queue_size):
        """
        Constructor
        """
        super().__init__()

        self.__inhibit_publishing = bool(inhibit_publishing)
        self.__queue_size = int(queue_size)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def inhibit_publishing(self):
        return self.__inhibit_publishing


    @property
    def queue_size(self):
        return self.__queue_size


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['inhibit-publishing'] = self.inhibit_publishing
        jdict['queue-size'] = self.queue_size

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTConf:{inhibit_publishing:%s, queue_size:%s}" %  (self.inhibit_publishing, self.queue_size)
