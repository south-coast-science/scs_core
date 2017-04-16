"""
Created on 22 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

schemas:
{"id": 34, "name": "south-coast-science-gasses-NO2-CO-SO2-H2S", "description": "South Coast Science Air Quality Sensor"}
{"id": 35, "name": "south-coast-science-gasses-NO2-Ox-CO-SO2", "description": "South Coast Science Air Quality Sensor"}
{"id": 28, "name": "south-coast-science-gasses-Ox-NO2-NO-CO", "description": "South Coast Science Air Quality Sensor"}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SourceSchema(JSONable):
    """
    classdocs
    """

    __SCHEMAS = None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.__SCHEMAS = {
            ('NO2', 'O3', 'NO', 'CO'): SourceSchema(28, 'NO2, O3, NO, CO'),
            ('NO2', 'O3', 'CO', 'SO2'): SourceSchema(35, 'NO2, O3, CO, SO2'),
            ('NO2', 'CO', 'SO2', 'H2S'): SourceSchema(34, 'NO2, CO, SO2, H2S'),
            ('CO', 'SO2', 'H2S', 'VOC'): SourceSchema(None, 'CO, SO2, H2S, VOCs'),
        }


    @classmethod
    def find(cls, gas_names):
        if gas_names is None:
            return None

        for schema_gas_names, schema in cls.__SCHEMAS.items():
            if set(schema_gas_names) == set(gas_names):
                return schema

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, schema_id, description):
        """
        Constructor
        """
        self.__schema_id = schema_id            # int
        self.__description = description        # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['schema_id'] = self.schema_id
        jdict['description'] = self.description

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def schema_id(self):
        return self.__schema_id


    @property
    def description(self):
        return self.__description


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SourceSchema:{schema_id:%s, description:%s}" % (self.schema_id, self.description)
