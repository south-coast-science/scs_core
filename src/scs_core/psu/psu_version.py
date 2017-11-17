"""
Created on 8 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"id": "South Coast Science PSU", "tag": "1.0.0", "c-date": "Aug  8 2017", "c-time": "08:35:25"}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PSUVersion(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        id = jdict.get('id')
        tag = jdict.get('tag')

        compile_date = jdict.get('c-date')
        compile_time = jdict.get('c-time')

        return PSUVersion(id, tag, compile_date, compile_time)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, tag, compile_date, compile_time):
        """
        Constructor
        """
        self.__id = id
        self.__tag = tag

        self.__compile_date = compile_date
        self.__compile_time = compile_time


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['id'] = self.id
        jdict['tag'] = self.tag

        jdict['c-date'] = self.compile_date
        jdict['c-time'] = self.compile_time

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def tag(self):
        return self.__tag


    @property
    def compile_date(self):
        return self.__compile_date


    @property
    def compile_time(self):
        return self.__compile_time


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUVersion:{id:%s, tag:%s, compile_date:%s, compile_time:%s}" \
               % (self.id, self.tag, self.compile_date, self.compile_time)
