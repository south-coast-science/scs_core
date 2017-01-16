'''
Created on 10 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class TopicInfo(JSONable):
    '''
    classdocs
   '''

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        format = jdict.get('format')
        type = jdict.get('type')
        schema = jdict.get('schema')
        graph_path = jdict.get('graph-path')

        return TopicInfo(format, type, schema, graph_path)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, format, type, schema, graph_path):
        '''
        Constructor
        '''
        self.__format = format              # string
        self.__type = type                  # string
        self.__schema = schema              # string
        self.__graph_path = graph_path      # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.format:
            jdict['format'] = self.format

        if self.format:
            jdict['type'] = self.type

        if self.format:
            jdict['schema'] = self.schema

        if self.format:
            jdict['graph-path'] = self.graph_path

        return jdict


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
