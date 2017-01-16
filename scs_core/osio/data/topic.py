"""
Created on 10 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

deliver-change
870725f3-e692-4538-aa81-bfa8b51d44e7

south-coast-science-dev
43308b72-ad41-4555-b075-b4245c1971db
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.osio.data.topic_info import TopicInfo


# --------------------------------------------------------------------------------------------------------------------

class Topic(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def find_for_org(cls, http_client, api_key, org_id):
        finder = TopicFinder(http_client, api_key)

        return finder.find_for_org(org_id)


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

        topic_info = TopicInfo.construct_from_jdict(jdict.get('topic_info'))

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

        jdict['path'] = self.path
        jdict['name'] = self.name
        jdict['description'] = self.description

        jdict['public'] = self.is_public
        jdict['rollups-enabled'] = self.is_public

        jdict['topic-info'] = self.topic_info.as_json()
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
        return "Topic:{path:%s, name:%s, description:%s, is_public:%s, rollups_enabled:%s, topic_info:%s, schema_id:%s}" % \
               (self.path, self.name, self.description, self.is_public, self.rollups_enabled, self.topic_info, self.schema_id)


# --------------------------------------------------------------------------------------------------------------------

from scs_core.osio.finder.topic_finder import TopicFinder
