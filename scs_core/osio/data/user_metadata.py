"""
Created on 30 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
  "id": "southcoastscience-dev",
  "name": "South Coast Science - Dev",
  "month": "2016-11",
  "gravatar-hash": "07f512e9fe64863039df0c0f1834cc25",
  "topics": [
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
    ]}
"""

from scs_core.osio.data.user import User
from scs_core.osio.data.user_topic import UserTopic


# --------------------------------------------------------------------------------------------------------------------

class UserMetadata(User):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # User...
        id = jdict.get('id')
        name = jdict.get('name')

        start = jdict.get('month')

        # UserMetadata...
        gravatar_hash = jdict.get('gravatar-hash')

        topics = [UserTopic.construct_from_jdict(topic_jdict) for topic_jdict in jdict.get('topics')]

        return UserMetadata(id, name, None, None, start, gravatar_hash, topics)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, name, email, password, start, gravatar_hash, topics):
        """
        Constructor
        """

        # User...
        User.__init__(self, id, name, email, password, start)

        # UserMetadata...
        self.__gravatar_hash = gravatar_hash            # string
        self.__topics = topics                          # list of UserTopic


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = User.as_json(self)

        jdict['gravatar-hash'] = self.gravatar_hash
        jdict['topics'] = self.topics

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def gravatar_hash(self):
        return self.__gravatar_hash


    @property
    def topics(self):
        return self.__topics


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        topics = '[' + ', '.join(str(topic) for topic in self.topics) + ']'

        return "UserMetadata:{id:%s, name:%s, email:%s, password:%s, start:%s, gravatar_hash:%s, topics:%s}" % \
               (self.id, self.name, self.email, self.password, self.start, self.gravatar_hash, topics)
