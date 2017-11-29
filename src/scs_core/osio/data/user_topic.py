"""
Created on 30 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
    {
      "topic": "/orgs/south-coast-science-dev/user/device/alpha-pi-eng-000100/status",
      "name": "Device status",
      "description": "lat (deg), lng (deg) GPS qual, DFE temp (Centigrade), host temp (Centigrade), errors",
      "public": true,
      "topic-info": {
        "format": "application/json"
      },
      "unit": null,
      "stats": {
        "period": 0,
        "last-reading": "55 days ago",
        "contributors": [
          {
            "name": "South Coast Science - Dev",
            "id": "southcoastscience-dev",
            "gravatar-hash": "07f512e9fe64863039df0c0f1834cc25"
          }
        ],
        "last-location": {
          "lat": 50.82313,
          "lon": -0.122922
        }
      },
      "owner-gravatar-hash": "d92c0a697bf3658745447e1a9467b506"
    }
"""

from scs_core.osio.data.abstract_topic import AbstractTopic
from scs_core.osio.data.topic_info import TopicInfo
from scs_core.osio.data.topic_stats import TopicStats


# --------------------------------------------------------------------------------------------------------------------

class UserTopic(AbstractTopic):
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

        # UserTopic...
        unit = jdict.get('unit')
        stats = TopicStats.construct_from_jdict(jdict.get('stats'))

        owner_gravatar_hash = jdict.get('owner-gravatar-hash')

        return UserTopic(path, name, description, is_public, info, unit, stats, owner_gravatar_hash)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, name, description, is_public, info,
                 unit, stats, owner_gravatar_hash):
        """
        Constructor
        """

        # AbstractTopic...
        AbstractTopic.__init__(self, path, name, description, is_public, info)

        # UserTopic...
        self.__unit = unit                                      # string
        self.__stats = stats                                    # TopicStats
        self.__owner_gravatar_hash = owner_gravatar_hash        # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = AbstractTopic.as_json(self)

        jdict['unit'] = self.unit
        jdict['stats'] = self.stats
        jdict['owner-gravatar-hash'] = self.owner_gravatar_hash

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def unit(self):
        return self.__unit


    @property
    def stats(self):
        return self.__stats


    @property
    def owner_gravatar_hash(self):
        return self.__owner_gravatar_hash


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UserTopic:{path:%s, name:%s, description:%s, is_public:%s, info:%s, " \
               "unit:%s, stats:%s, owner_gravatar_hash:%s}" % \
               (self.path, self.name, self.description, self.is_public, self.info,
                self.unit, self.stats, self.owner_gravatar_hash)
