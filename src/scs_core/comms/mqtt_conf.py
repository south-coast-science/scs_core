"""
Created on 17 May 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"inhibit-publishing": false, "report-file": "/tmp/southcoastscience/mqtt_queue_report.json", "debug": true}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class MQTTConf(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "mqtt_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return MQTTConf(False, None, False) if skeleton else None

        inhibit_publishing = jdict.get('inhibit-publishing', False)
        report_file = jdict.get('report-file', None)
        debug = jdict.get('debug', False)

        return MQTTConf(inhibit_publishing, report_file, debug)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, inhibit_publishing, report_file, debug):
        """
        Constructor
        """
        super().__init__()

        self.__inhibit_publishing = bool(inhibit_publishing)                # do not attempt to publish
        self.__report_file = report_file                                    # tmp file to store current queue length
        self.__debug = bool(debug)                                          # DEBUG log level


    def __eq__(self, other):
        try:
            return self.inhibit_publishing == other.inhibit_publishing and self.report_file == other.report_file and \
                   self.debug == other.debug

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def inhibit_publishing(self):
        return self.__inhibit_publishing


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
        jdict['report-file'] = self.report_file
        jdict['debug'] = self.debug

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTConf:{inhibit_publishing:%s, report_file:%s, debug:%s}" %  \
               (self.inhibit_publishing, self.report_file, self.debug)
