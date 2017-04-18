"""
Created on 22 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

schemas:
{"id": 34, "name": "south-coast-science-gasses-NO2-CO-SO2-H2S", "description": "..."}
{"id": 35, "name": "south-coast-science-gasses-NO2-Ox-CO-SO2", "description": "..."}
{"id": 28, "name": "south-coast-science-gasses-Ox-NO2-NO-CO", "description": "..."}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ProjectTopic(JSONable):
    """
    classdocs
    """

    CLIMATE = None
    PARTICULATES = None
    STATUS = None
    CONTROL = None

    __GAS_SCHEMAS = {}

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

        cls.__GAS_SCHEMAS = {
            ('NO2', 'Ox', 'NO', 'CO'):
                ProjectTopic(28, 'Gas concentrations',
                             'Pt1000 temp, internal SHT', ('NO2', 'O3', 'NO', 'CO')),

            ('NO2', 'Ox', 'CO', 'SO2'):
                ProjectTopic(35, 'Gas concentrations',
                             'Pt1000 temp, internal SHT', ('NO2', 'O3', 'CO', 'SO2')),

            ('NO2', 'CO', 'SO2', 'H2S'):
                ProjectTopic(34, 'Gas concentrations',
                             'Pt1000 temp, internal SHT', ('NO2', 'CO', 'SO2', 'H2S')),

            ('NO2', 'Ox', 'CO', 'VOC'):                         # TODO: request an OSIO schema
                ProjectTopic(None, 'Gas concentrations',
                             'NO2, O3, CO, VOC electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                             'Pt1000 temp, internal SHT', ('NO2', 'O3', 'CO', 'VOC')),

            ('CO', 'SO2', 'H2S', 'VOC'):                        # TODO: request an OSIO schema
                ProjectTopic(None, 'Gas concentrations',
                             'CO, SO2, H2S, VOCs electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                             'Pt1000 temp, internal SHT', ('CO', 'SO2', 'H2S', 'VOC'))
        }


    @classmethod
    def find_gas_schema(cls, gas_names):
        if gas_names is None:
            return None

        for schema_gas_names, schema in cls.__GAS_SCHEMAS.items():
            if set(schema_gas_names) == set(gas_names):
                return schema

        return None


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
