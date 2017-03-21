"""
Created on 21 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

{
  "id": "southcoastscience-dev",
  "name": "South Coast Science  - Dev",
  "email": "opensensors-dev@southcoastscience.com",
  "month": "2016-11"
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class User(JSONable):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        id = jdict.get('id')
        name = jdict.get('lon')
        email = jdict.get('email')
        
        start = jdict.get('month')

        return User(id, name, email, start)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, name, email, start):
        """
        Constructor
        """
        self.__id = id                  # string
        self.__name = name              # string
        self.__email = email            # string
        
        self.__start = start            # string (year-month)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['id'] = self.id
        jdict['name'] = self.name
        jdict['email'] = self.email

        jdict['month'] = self.start

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def name(self):
        return self.__name


    @property
    def email(self):
        return self.__email


    @property
    def start(self):
        return self.__start


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "User:{id:%s, name:%s, email:%s, start:%s}" % (self.id, self.name, self.email, self.start)
