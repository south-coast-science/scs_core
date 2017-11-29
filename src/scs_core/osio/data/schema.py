"""
Created on 14 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
    "id": 28,
    "name": "south-coast-science-gases-Ox-NO2-NO-CO",
    "description": "South Coast Science Air Quality Sensor; concentration of gases"
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Schema(JSONable):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        id = jdict.get('id')
        name = jdict.get('name')
        description = jdict.get('description')

        return Schema(id, name, description)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, name, description):
        """
        Constructor
        """
        self.__id = id                          # int
        self.__name = name                      # string
        self.__description = description        # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['id'] = self.id
        jdict['name'] = self.name

        if self.description is not None:
            jdict['description'] = self.description

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def name(self):
        return self.__name


    @property
    def description(self):
        return self.__description


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Schema:{id:%s, name:%s, description:%s}" % (self.id, self.name, self.description)
