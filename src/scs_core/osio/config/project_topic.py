"""
Created on 22 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

schemas:
{"id": 33, "name": "south-coast-science-climate",
"description": "South Coast Science Air Quality Sensor; climate"}

{"id": 29, "name": "south-coast-science-particulates", "description":
"South Coast Science Air Quality Sensor; particulates"}


{"id": 28, "name": "south-coast-science-gasses-Ox-NO2-NO-CO",
"description": "South Coast Science Air Quality Sensor; concentration of gasses"}

{"id": 34, "name": "south-coast-science-gasses-NO2-CO-SO2-H2S",
"description": "South Coast Science Air Quality Sensor; concentration of gasses"}

{"id": 35, "name": "south-coast-science-gasses-NO-Ox-CO-SO2",
"description": "South Coast Science Air Quality Sensor; concentration of gasses"}

{"id": 39, "name": "south-coast-science-gasses-NO2-Ox-CO-SO2",
"description": "South Coast Science Air Quality Sensor; concentration of gasses"}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# TODO: fix for CO2

# --------------------------------------------------------------------------------------------------------------------

class ProjectTopic(JSONable):
    """
    classdocs
    """

    CLIMATE = None
    PARTICULATES = None
    STATUS = None
    CONTROL = None
    EMPTY_GASES_TOPIC = None

    __GASES_TOPICS = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.CLIMATE = ProjectTopic(33, 'Climate',
                                   'temperature (Centigrade), relative humidity (%)', ('temperature', 'humidity'))

        cls.PARTICULATES = ProjectTopic(29, 'Particulate densities',
                                        'PM1 (ug/m3), PM2.5 (ug/m3), PM10 (ug/m3), bin counts, mtf1, mtf3, mtf5 mtf7',
                                        ('PM1', 'PM2.5', 'PM10'))

        cls.STATUS = ProjectTopic(None, 'Device status',
                                  'lat (deg), lng (deg) GPS qual, DFE temp (Centigrade), host temp (Centigrade), ' 
                                  'errors', ())

        cls.CONTROL = ProjectTopic(None, 'Device control',
                                   'this topic is subscribed to by the device for control purposes', ())

        cls.__GASES_TOPICS = {
            ('NO2', 'Ox', 'NO', 'CO'):
                ProjectTopic(28, 'Gas concentrations',
                             'NO2, O3, NO, CO electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                             'Pt1000 temp, internal SHT', ('NO2', 'O3', 'NO', 'CO')),

            ('NO2', 'CO', 'SO2', 'H2S'):
                ProjectTopic(34, 'Gas concentrations',
                             'NO2, CO, SO2, H2S electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                             'Pt1000 temp, internal SHT', ('NO2', 'CO', 'SO2', 'H2S')),

            ('NO', 'Ox', 'CO', 'SO2'):                          # not a standard Alphasense configuration
                ProjectTopic(35, 'Gas concentrations',
                             'NO2, O3, CO, SO2 electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                             'Pt1000 temp, internal SHT', ('NO', 'O3', 'CO', 'SO2')),

            ('NO2', 'Ox', 'CO', 'SO2'):
                ProjectTopic(39, 'Gas concentrations',
                             'NO2, O3, CO, SO2 electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                             'Pt1000 temp, internal SHT', ('NO2', 'O3', 'CO', 'SO2')),

            ('NO2', 'Ox', 'CO', 'VOC'):                         # TODO: request an OSIO schema
                ProjectTopic(None, 'Gas concentrations',
                             'NO2, O3, CO, VOC electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                             'Pt1000 temp, internal SHT', ('NO2', 'O3', 'CO', 'VOC')),

            ('CO', 'SO2', 'H2S', 'VOC'):                        # TODO: request an OSIO schema
                ProjectTopic(None, 'Gas concentrations',
                             'CO, SO2, H2S, VOCs electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                             'Pt1000 temp, internal SHT', ('CO', 'SO2', 'H2S', 'VOC')),

            ('SN1', 'SN2', 'SN3', 'SN4'):
                ProjectTopic(None, 'Test load',
                             'electrochemical we (V), ae (V), '
                             'Pt1000 temp, internal SHT', ('test',))
        }

        cls.EMPTY_GASES_TOPIC = ProjectTopic(None, 'Gas concentrations',
                                             'no information available', ())


    @classmethod
    def get_gases_topic(cls, gas_names):
        if gas_names is None:
            return cls.EMPTY_GASES_TOPIC

        for topic_gas_names, topic in cls.__GASES_TOPICS.items():
            if set(topic_gas_names) == set(gas_names):
                return topic

        return cls.EMPTY_GASES_TOPIC


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, schema_id, name, description, tags):
        """
        Constructor
        """
        self.__schema_id = schema_id            # int
        self.__name = name                      # string
        self.__description = description        # string
        self.__tags = tags                      # sequence of string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['schema-id'] = self.schema_id
        jdict['name'] = self.name
        jdict['description'] = self.description
        jdict['tags'] = self.tags

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def schema_id(self):
        return self.__schema_id


    @property
    def name(self):
        return self.__name


    @property
    def description(self):
        return self.__description


    @property
    def tags(self):
        return self.__tags


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ProjectTopic:{schema_id:%s, name:%s, tags:%s, description:%s}" % \
               (self.schema_id, self.name, self.tags, self.description)
