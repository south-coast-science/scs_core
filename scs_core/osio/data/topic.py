"""
Created on 10 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
  "description": "electrochemical we (V), ae (V), wc (V), cnc (ppb), Pt100 temp, internal SHT",
  "unit": null,
  "derived-topics": [
    {
      "description": "electrochemical we (V), ae (V), wc (V), cnc (ppb), Pt100 temp, internal SHT",
      "unit": null,
      "name": "15min statistics of Gas concentrations",
      "public": true,
      "topic": "/osio/orgs/south-coast-science-dev/production-test/loc/1/gases/15min",
      "derived-data": {
        "interval": 900
      },
      "topic-info": {
        "format": "application/json"
      }
    },
    {
      "description": "electrochemical we (V), ae (V), wc (V), cnc (ppb), Pt100 temp, internal SHT",
      "unit": null,
      "name": "5min statistics of Gas concentrations",
      "public": true,
      "topic": "/osio/orgs/south-coast-science-dev/production-test/loc/1/gases/5min",
      "derived-data": {
        "interval": 300
      },
      "topic-info": {
        "format": "application/json"
      }
    },
    {
      "description": "electrochemical we (V), ae (V), wc (V), cnc (ppb), Pt100 temp, internal SHT",
      "unit": null,
      "name": "hourly statistics of Gas concentrations",
      "public": true,
      "topic": "/osio/orgs/south-coast-science-dev/production-test/loc/1/gases/hourly",
      "derived-data": {
        "interval": 3600
      },
      "topic-info": {
        "format": "application/json"
      }
    }
  ],
  "name": "Gas concentrations",
  "public": true,
  "topic": "/orgs/south-coast-science-dev/production-test/loc/1/gases",
  "topic-info": {
    "format": "application/json"
  },
  "bookmark-count": 0,
  "stats": {
    "period": 604800,
    "last-reading": "5 seconds ago",
    "average-frequency": "9 seconds",
    "total": 49661,
    "contributors": [
      {
        "name": "South Coast Science - Dev",
        "id": "southcoastscience-dev",
        "gravatar-hash": "07f512e9fe64863039df0c0f1834cc25"
      }
    ],
    "last-location": {
      "lat": 50.819456,
      "lon": -0.128336
    }
  }
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.osio.data.topic_info import TopicInfo


# TODO: update class to receive full topic metadata

# --------------------------------------------------------------------------------------------------------------------

class Topic(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        path = jdict.get('topic')
        name = jdict.get('name')
        description = jdict.get('description')

        is_public = jdict.get('public')
        rollups_enabled = jdict.get('rollups-enabled')

        topic_info = TopicInfo.construct_from_jdict(jdict.get('topic-info'))

        schema_id = jdict.get('schema-id', 0)

        return Topic(path, name, description, is_public, rollups_enabled, topic_info, schema_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, name, description, is_public, rollups_enabled, topic_info, schema_id):
        """
        Constructor
        """
        self.__path = path                          # string
        self.__name = name                          # string
        self.__description = description            # string

        self.__is_public = is_public                # bool
        self.__rollups_enabled = rollups_enabled    # bool

        self.__topic_info = topic_info              # TopicInfo
        self.__schema_id = schema_id                # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['topic'] = self.path
        jdict['name'] = self.name
        jdict['description'] = self.description

        jdict['public'] = self.is_public
        jdict['rollups-enabled'] = self.is_public

        jdict['topic-info'] = self.topic_info

        if self.schema_id:
            jdict['schema-id'] = self.schema_id

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


    @property
    def name(self):
        return self.__name


    @property
    def description(self):
        return self.__description


    @property
    def is_public(self):
        return self.__is_public


    @property
    def rollups_enabled(self):
        return self.__rollups_enabled


    @property
    def topic_info(self):
        return self.__topic_info


    @property
    def schema_id(self):
        return self.__schema_id


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Topic:{path:%s, name:%s, description:%s, is_public:%s, rollups_enabled:%s, topic_info:%s, " \
               "schema_id:%s}" % \
               (self.path, self.name, self.description, self.is_public, self.rollups_enabled, self.topic_info,
                self.schema_id)
