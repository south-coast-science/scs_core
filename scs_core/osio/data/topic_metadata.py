"""
Created on 2 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
  "description": "electrochemical we (V), ae (V), wc (V), cnc (ppb), Pt100 temp, internal SHT",
  "unit": null,
  "derived-topics": [
    {
      "stats": "electrochemical we (V), ae (V), wc (V), cnc (ppb), Pt100 temp, internal SHT",
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

from scs_core.osio.data.abstract_topic import AbstractTopic
from scs_core.osio.data.topic_info import TopicInfo


# --------------------------------------------------------------------------------------------------------------------

class TopicMetadata(AbstractTopic):
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

        # TopicMetadata...
        derived_topics = None       # TODO: implement
        bookmark_count = None       # TODO: implement
        stats = None                # TODO: implement

        return TopicMetadata(path, name, description, is_public, topic_info, derived_topics, bookmark_count, stats)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, name, description, is_public, topic_info,
                 derived_topics, bookmark_count, stats):
        """
        Constructor
        """

        # AbstractTopic...
        AbstractTopic.__init__(self, path, name, description, is_public, topic_info)

        # TopicMetadata...
        self.__derived_topics = derived_topics              # list of DerivedTopic
        self.__bookmark_count = bookmark_count              # int
        self.__stats = stats                                # TopicStats


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        # AbstractTopic...              # TODO: put these on superclass
        jdict['topic'] = self.path
        jdict['name'] = self.name
        jdict['description'] = self.description

        jdict['public'] = self.is_public

        jdict['topic-info'] = self.topic_info

        # TopicMetadata...
        jdict['derived-topics'] = self.derived_topics
        jdict['bookmark-count'] = self.bookmark_count
        jdict['stats'] = self.stats

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
        return "TopicMetadata:{path:%s, name:%s, description:%s, is_public:%s, topic_info:%s, " \
               "derived_topics:%s, bookmark_count:%s, stats:%s}" % \
               (self.path, self.name, self.description, self.is_public, self.topic_info,
                self.derived_topics, self.bookmark_count, self.stats)
