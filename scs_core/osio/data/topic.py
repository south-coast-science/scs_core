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

from collections import OrderedDict

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

        topic_info = TopicInfo.construct_from_jdict(jdict.get('topic-info'))

        # Topic...
        rollups_enabled = jdict.get('rollups-enabled')
        schema_id = jdict.get('schema-id')

        return Topic(path, name, description, is_public, topic_info, rollups_enabled, schema_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, name, description, is_public, topic_info,
                 rollups_enabled, schema_id):
        """
        Constructor
        """
        # AbstractTopic...
        AbstractTopic.__init__(self, path, name, description, is_public, topic_info)

        # Topic...
        self.__rollups_enabled = rollups_enabled        # bool
        self.__schema_id = schema_id                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        # AbstractTopic...
        jdict['topic'] = self.path
        jdict['name'] = self.name
        jdict['description'] = self.description

        jdict['public'] = self.is_public

        jdict['topic-info'] = self.topic_info

        # Topic...
        jdict['rollups-enabled'] = self.is_public

        if self.schema_id:
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
        return "Topic:{path:%s, name:%s, description:%s, is_public:%s, topic_info:%s, " \
               "rollups_enabled:%s, schema_id:%s}" % \
               (self.path, self.name, self.description, self.is_public, self.topic_info,
                self.rollups_enabled, self.schema_id)
