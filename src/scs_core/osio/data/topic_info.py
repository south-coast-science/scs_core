"""
Created on 10 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
    "format": "application/json"
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class TopicInfo(JSONable):
    """
    classdocs
   """

    FORMAT_JSON = "application/json"
    FORMAT_TEXT = "text"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        topic_format = jdict.get('format')
        topic_type = jdict.get('type')
        schema = jdict.get('schema')
        graph_path = jdict.get('graph-path')

        return TopicInfo(topic_format, topic_type, schema, graph_path)


    # ----------------------------------------------------------------------------------------------------------------
    # for the v2 API, schema_id goes in Topic...

    def __init__(self, topic_format, topic_type=None, schema=None, graph_path=None):
        """
        Constructor
        """
        self.__format = topic_format        # string
        self.__type = topic_type            # string
        self.__schema = schema              # string
        self.__graph_path = graph_path      # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.format:
            jdict['format'] = self.format

        if self.type:
            jdict['type'] = self.type

        if self.schema:
            jdict['schema'] = self.schema

        if self.graph_path:
            jdict['graph-path'] = self.graph_path

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def schema_id(self):
        if self.__schema is None:
            return None

        return self.__schema.id


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def format(self):
        return self.__format


    @property
    def type(self):
        return self.__type


    @property
    def schema(self):
        return self.__schema


    @property
    def graph_path(self):
        return self.__graph_path


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicInfo:{format:%s, type:%s, schema:%s, graph_path:%s}" % \
                    (self.format, self.type, self.schema, self.graph_path)
