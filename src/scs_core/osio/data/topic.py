"""
Created on 10 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
    {
      "name": "Device status",
      "description": "lat (deg), lng (deg) GPS qual, DFE temp (Centigrade), host temp (Centigrade), errors",
      "topic": "/orgs/south-coast-science-dev/development/device/alpha-pi-eng-000007/status",
      "public": true,
      "rollups-enabled": true,
      "topic-info": {
        "format": "application/json"
      }
    }
"""

from scs_core.osio.data.abstract_topic import AbstractTopic
from scs_core.osio.data.topic_info import TopicInfo


# --------------------------------------------------------------------------------------------------------------------

class Topic(AbstractTopic):
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

        # Topic...
        rollups_enabled = jdict.get('rollups-enabled')
        schema_id = jdict.get('schema-id')

        return Topic(path, name, description, is_public, info, rollups_enabled, schema_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, name, description, is_public, info, rollups_enabled, schema_id):
        """
        Constructor
        """
        # AbstractTopic...
        AbstractTopic.__init__(self, path, name, description, is_public, info)

        # Topic...
        self.__rollups_enabled = rollups_enabled        # bool
        self.__schema_id = schema_id                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = AbstractTopic.as_json(self)

        if self.rollups_enabled is not None:
            jdict['rollups-enabled'] = self.rollups_enabled

        if self.schema_id is not None:
            jdict['schema-id'] = self.schema_id

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rollups_enabled(self):
        return self.__rollups_enabled


    @property
    def schema_id(self):
        return self.__schema_id


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Topic:{path:%s, name:%s, description:%s, is_public:%s, info:%s, rollups_enabled:%s, schema_id:%s}" % \
               (self.path, self.name, self.description, self.is_public, self.info, self.rollups_enabled, self.schema_id)
