"""
Created on 17 May 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"inhibit-publishing": false, "queue-size": 21000, "report-file": "/tmp/southcoastscience/mqtt_queue_length.json"}
"""

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
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return MQTTConf(False, cls.DEFAULT_QUEUE_SIZE, None, False)

        inhibit_publishing = jdict.get('inhibit-publishing', False)
        queue_size = jdict.get('queue-size', cls.DEFAULT_QUEUE_SIZE)
        report_file = jdict.get('report-file', None)
        debug = jdict.get('debug', False)

        return MQTTConf(inhibit_publishing, queue_size, report_file, debug)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, inhibit_publishing, queue_size, report_file, debug):
        """
        Constructor
        """
        super().__init__()

        self.__inhibit_publishing = bool(inhibit_publishing)                # do not attempt to publish
        self.__queue_size = int(queue_size)                                 # maximum queue size
        self.__report_file = report_file                                    # tmp file to store current queue length
        self.__debug = bool(debug)                                          # DEBUG log level


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def inhibit_publishing(self):
        return self.__inhibit_publishing


    @property
    def queue_size(self):
        return self.__queue_size


    @property
    def report_file(self):
        return self.__report_file


    @property
    def debug(self):
        return self.__debug


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['inhibit-publishing'] = self.inhibit_publishing
        jdict['queue-size'] = self.queue_size
        jdict['report-file'] = self.report_file
        jdict['debug'] = self.debug

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTConf:{inhibit_publishing:%s, queue_size:%s, report_file:%s, debug:%s}" %  \
               (self.inhibit_publishing, self.queue_size, self.report_file, self.debug)
