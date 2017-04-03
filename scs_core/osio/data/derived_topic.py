"""
Created on 10 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
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
"""

from collections import OrderedDict

from scs_core.osio.data.abstract_topic import AbstractTopic
from scs_core.osio.data.topic_info import TopicInfo


# --------------------------------------------------------------------------------------------------------------------

class DerivedTopic(AbstractTopic):
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

        # DerivedTopic...
        unit = jdict.get('unit')
        derived_data = jdict.get('derived-data')

        return DerivedTopic(path, name, description, is_public, topic_info, unit, derived_data)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, name, description, is_public, topic_info,
                 unit, derived_data):
        """
        Constructor
        """
        # AbstractTopic...
        AbstractTopic.__init__(self, path, name, description, is_public, topic_info)

        # DerivedTopic...
        self.__unit = unit                          # string
        self.__derived_data = derived_data          # DerivedData


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        # AbstractTopic...
        jdict['topic'] = self.path
        jdict['name'] = self.name
        jdict['description'] = self.description

        jdict['public'] = self.is_public

        jdict['topic-info'] = self.topic_info

        # DerivedTopic...
        jdict['unit'] = self.unit
        jdict['derived-data'] = self.derived_data

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def unit(self):
        return self.__unit


    @property
    def derived_data(self):
        return self.__derived_data


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DerivedTopic:{path:%s, name:%s, description:%s, is_public:%s, topic_info:%s, " \
               "unit:%s, derived_data:%s}" % \
               (self.path, self.name, self.description, self.is_public, self.topic_info,
                self.unit, self.derived_data)
