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

class ProjectSchema(JSONable):
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
        cls.CLIMATE = ProjectSchema(33, 'Climate',
                                    'temperature (Centigrade), relative humidity (%)')

        cls.PARTICULATES = ProjectSchema(29, 'Particulate densities',
                                         'PM1 (ug/m3), PM2.5 (ug/m3), PM10 (ug/m3), bin counts, mtf1, mtf3, mtf5 mtf7')

        cls.STATUS = ProjectSchema(None, 'Device status',
                                   'lat (deg), lng (deg) GPS qual, DFE temp (Centigrade), host temp (Centigrade), '
                                   'errors')

        cls.CONTROL = ProjectSchema(None, 'Device control',
                                    'this topic is subscribed to by the device for control purposes')

        cls.__GAS_SCHEMAS = {
            ('NO2', 'O3', 'NO', 'CO'):
                ProjectSchema(28, 'Gas concentrations',
                              'NO2, O3, NO, CO electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                              'Pt1000 temp, internal SHT'),

            ('NO2', 'O3', 'CO', 'SO2'):
                ProjectSchema(35, 'Gas concentrations',
                              'NO2, O3, CO, SO2 electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                              'Pt1000 temp, internal SHT'),

            ('NO2', 'CO', 'SO2', 'H2S'):
                ProjectSchema(34, 'Gas concentrations',
                              'NO2, CO, SO2, H2S electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                              'Pt1000 temp, internal SHT'),

            ('CO', 'SO2', 'H2S', 'VOC'):
                ProjectSchema(None, 'Gas concentrations',
                              'CO, SO2, H2S, VOCs electrochemical we (V), ae (V), wc (V), cnc (ppb), '
                              'Pt1000 temp, internal SHT'),
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

    def __init__(self, schema_id, name, description):
        """
        Constructor
        """
        self.__schema_id = schema_id            # int
        self.__name = name                      # string
        self.__description = description        # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['schema-id'] = self.schema_id
        jdict['name'] = self.name
        jdict['description'] = self.description

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


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ProjectSchema:{schema_id:%s, name:%s, description:%s}" % \
               (self.schema_id, self.name, self.description)
