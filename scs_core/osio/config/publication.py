"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Publication(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "osio_publication.json"

    @classmethod
    def filename(cls, host):
        return host.SCS_OSIO + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        gasses_topic = jdict.get('gasses')
        particulates_topic = jdict.get('particulates')
        climate_topic = jdict.get('climate')

        status_topic = jdict.get('status')      # TODO: construct from serial number?

        return Publication(gasses_topic, particulates_topic, climate_topic, status_topic)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gasses_topic, particulates_topic, climate_topic, status_topic):
        """
        Constructor
        """
        self.__gasses_topic = gasses_topic                  # string
        self.__particulates_topic = particulates_topic      # string
        self.__climate_topic = climate_topic                # string

        self.__status_topic = status_topic                  # string


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['gasses'] = self.gasses_topic
        jdict['particulates'] = self.particulates_topic
        jdict['climate'] = self.climate_topic

        jdict['status'] = self.status_topic

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def gasses_topic(self):
        return self.__gasses_topic


    @property
    def particulates_topic(self):
        return self.__particulates_topic


    @property
    def climate_topic(self):
        return self.__climate_topic


    @property
    def status_topic(self):
        return self.__status_topic


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Publication:{gasses_topic:%s, particulates_topic:%s, climate_topic:%s, status_topic:%s}" % \
               (self.gasses_topic, self.particulates_topic, self.climate_topic, self.status_topic)
