"""
Created on 6 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
    {
      "name": "Particulate densities",
      "description": "pm1 (ug/m3), pm2.5 (ug/m3), pm10 (ug/m3), bin counts, mtf1, mtf3, mtf5 mtf7",
      "topic": "/orgs/south-coast-science-dev/development/loc/1/particulates",
      "public": true,
      "schema": {
        "id": 29,
        "name": "south-coast-science-particulates"
      },
      "rollups-enabled": true,
      "topic-info": {
        "format": "application/json"
      }
    }
"""

from scs_core.osio.data.abstract_topic import AbstractTopic
from scs_core.osio.data.schema import Schema
from scs_core.osio.data.topic_info import TopicInfo


# --------------------------------------------------------------------------------------------------------------------

class TopicSummary(AbstractTopic):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # AbstractTopic...
        path = jdict.get('topic')
        name = jdict.get('name')
        description = jdict.get('description')

        is_public = jdict.get('public')

        info = TopicInfo.construct_from_jdict(jdict.get('topic-info'))

        # TopicSummary...
        rollups_enabled = jdict.get('rollups-enabled')
        schema = Schema.construct_from_jdict(jdict.get('schema'))

        return TopicSummary(path, name, description, is_public, info, rollups_enabled, schema)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, name, description, is_public, info,
                 rollups_enabled, schema):
        """
        Constructor
        """
        # AbstractTopic...
        AbstractTopic.__init__(self, path, name, description, is_public, info)

        # TopicSummary...
        self.__rollups_enabled = rollups_enabled        # bool
        self.__schema = schema                          # Schema


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = AbstractTopic.as_json(self)

        jdict['rollups-enabled'] = self.rollups_enabled

        if self.schema is not None:
            jdict['schema'] = self.schema

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def schema_id(self):
        if self.__schema is None:
            return None

        return self.__schema.id


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rollups_enabled(self):
        return self.__rollups_enabled


    @property
    def schema(self):
        return self.__schema


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicSummary:{path:%s, name:%s, description:%s, is_public:%s, info:%s, " \
               "rollups_enabled:%s, schema:%s}" % \
               (self.path, self.name, self.description, self.is_public, self.info,
                self.rollups_enabled, self.schema)
