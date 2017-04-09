"""
Created on 8 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
  "id": "south-coast-science-dev",
  "name": "South Coast Science  (dev)",
  "website": "https://www.southcoastscience.com/",
  "description": "Development operations for South Coast Science air quality monitoring instruments.",
  "email": "bruno.beloff@southcoastscience.com"
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Organisation(JSONable):
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
        website = jdict.get('website')
        description = jdict.get('description')
        email = jdict.get('email')

        return Organisation(id, name, website, description, email)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, name, website, description, email):
        """
        Constructor
        """
        self.__id = id                          # string
        self.__name = name                      # string
        self.__website = website                # string
        self.__description = description        # string
        self.__email = email                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.id is not None:
            jdict['id'] = self.id

        jdict['name'] = self.name
        jdict['website'] = self.website
        jdict['description'] = self.description
        jdict['email'] = self.email

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def name(self):
        return self.__name


    @property
    def website(self):
        return self.__website


    @property
    def description(self):
        return self.__description


    @property
    def email(self):
        return self.__email


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Organisation:{id:%s, name:%s, website:%s, description:%s, email:%s}" % \
               (self.id, self.name, self.website, self.description, self.email)
