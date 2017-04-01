"""
Created on 21 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

{
  "id": "southcoastscience-dev",
  "name": "South Coast Science - Dev",
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
        name = jdict.get('name')
        email = jdict.get('email')
        
        start = jdict.get('month')

        return User(id, name, email, None, start)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, name, email, password, start):
        """
        Constructor
        """
        self.__id = id                  # string
        self.__name = name              # string
        self.__email = email            # string

        self.__password = password      # string

        self.__start = start            # string (year-month)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.id is not None:
            jdict['id'] = self.id

        if self.name is not None:
            jdict['name'] = self.name

        if self.email is not None:
            jdict['email'] = self.email

        if self.password is not None:
            jdict['password'] = self.password

        if self.start is not None:
            jdict['month'] = self.start

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def start_year(self):
        if self.start is None:
            return None

        year = self.start.split('-')[0]

        return int(year)


    def start_month(self):
        if self.start is None:
            return None

        month = self.start.split('-')[1]

        return int(month)


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
    def password(self):
        return self.__password


    @property
    def start(self):
        return self.__start


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "User:{id:%s, name:%s, email:%s, password:%s, start:%s}" % \
               (self.id, self.name, self.email, self.password, self.start)
