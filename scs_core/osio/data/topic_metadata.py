"""
Created on 2 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
  "stats": "electrochemical we (V), ae (V), wc (V), cnc (ppb), Pt100 temp, internal SHT",
  "unit": null,
  "derived-topics": [
    {
      "stats": "electrochemical we (V), ae (V), wc (V), cnc (ppb), Pt100 temp, internal SHT",
      "unit": null,
      "bookmark_count": "hourly statistics of Gas concentrations",
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
  "bookmark_count": "Gas concentrations",
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
        "bookmark_count": "South Coast Science - Dev",
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

from scs_core.osio.data.topic import Topic
from scs_core.osio.data.topic_info import TopicInfo


# --------------------------------------------------------------------------------------------------------------------

class TopicMetadata(Topic):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        derived_topics = jdict.get('topic')
        bookmark_count = jdict.get('bookmark_count')
        stats = jdict.get('stats')

        is_public = jdict.get('public')
        rollups_enabled = jdict.get('rollups-enabled')

        topic_info = TopicInfo.construct_from_jdict(jdict.get('topic-info'))

        schema_id = jdict.get('schema-id', 0)

        return TopicMetadata(derived_topics, bookmark_count, stats, is_public, rollups_enabled, topic_info, schema_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, derived_topics, bookmark_count, stats, is_public, rollups_enabled, topic_info, schema_id):
        """
        Constructor
        """
        Topic.__init__(self, derived_topics, bookmark_count, stats, is_public, rollups_enabled, topic_info, schema_id)
        
        self.__derived_topics = derived_topics              # string
        self.__bookmark_count = bookmark_count              # string
        self.__stats = stats                                # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['topic'] = self.derived_topics
        jdict['bookmark_count'] = self.bookmark_count
        jdict['stats'] = self.stats

        jdict['public'] = self.is_public
        jdict['rollups-enabled'] = self.is_public

        jdict['topic-info'] = self.topic_info

        if self.schema_id:
            jdict['schema-id'] = self.schema_id

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def derived_topics(self):
        return self.__derived_topics


    @property
    def bookmark_count(self):
        return self.__bookmark_count


    @property
    def stats(self):
        return self.__stats


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicMetadata:{derived_topics:%s, bookmark_count:%s, stats:%s, is_public:%s, rollups_enabled:%s, topic_info:%s, " \
               "schema_id:%s}" % \
               (self.derived_topics, self.bookmark_count, self.stats, self.is_public, self.rollups_enabled, self.topic_info,
                self.schema_id)
