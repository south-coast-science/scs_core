"""
Created on 17 May 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"inhibit-publishing": false, "debug": true}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class MQTTConf(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __REPORT_FILENAME = "mqtt_queue_report.json"

    @classmethod
    def report_file(cls, manager):
        return manager.tmp_file(cls.__REPORT_FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "mqtt_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return MQTTConf(False, None) if skeleton else None

        inhibit_publishing = jdict.get('inhibit-publishing', False)
        debug = jdict.get('debug', False)

        return MQTTConf(inhibit_publishing, debug)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, inhibit_publishing, debug):
        """
        Constructor
        """
        super().__init__()

        self.__inhibit_publishing = bool(inhibit_publishing)                # do not attempt to publish
        self.__debug = bool(debug)                                          # DEBUG log level


    def __eq__(self, other):
        try:
            return self.inhibit_publishing == other.inhibit_publishing and self.debug == other.debug

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def inhibit_publishing(self):
        return self.__inhibit_publishing


    @property
    def debug(self):
        return self.__debug


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['inhibit-publishing'] = self.inhibit_publishing
        jdict['debug'] = self.debug

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTConf:{inhibit_publishing:%s, debug:%s}" %  \
               (self.inhibit_publishing, self.debug)
