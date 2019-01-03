"""
Created on 10 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
    "name": "South Coast Science - Dev",
    "id": "southcoastscience-dev",
    "gravatar-hash": "07f512e9fe64863039df0c0f1834cc25"
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class TopicContributor(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        name = jdict.get('name')
        id = jdict.get('id')
        gravatar_hash = jdict.get('gravatar-hash')

        return TopicContributor(name, id, gravatar_hash)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, id, gravatar_hash):
        """
        Constructor
        """
        self.__name = name                      # string
        self.__id = id                          # string
        self.__gravatar_hash = gravatar_hash    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['name'] = self.name
        jdict['id'] = self.id
        jdict['gravatar-hash'] = self.gravatar_hash

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def id(self):
        return self.__id


    @property
    def gravatar_hash(self):
        return self.__gravatar_hash


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicContributor:{name:%s, id:%s, gravatar_hash:%s}" % (self.name, self.id, self.gravatar_hash)
