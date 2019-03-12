"""
Created on 11 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"topic": "particulates", "species": "pm2p5", "schedule": "scs-particulates"}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class DatumMapping(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if jdict is None:
            return None

        topic = jdict.get('topic')
        species = jdict.get('species')
        schedule = jdict.get('schedule')

        return DatumMapping(topic, species, schedule)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, species, schedule):
        """
        Constructor
        """
        self.__topic = topic                                        # string
        self.__species = species                                    # string
        self.__schedule = schedule                                  # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['topic'] = self.topic
        jdict['species'] = self.species
        jdict['schedule'] = self.schedule

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    # TODO: look up source_mapping from (topic, species, source)


    # ----------------------------------------------------------------------------------------------------------------

    def tag(self, datum: PathDict):
        return datum.node(self.tag_path())


    def value(self, datum: PathDict):
        return datum.node(self.species_path())


    def source(self, datum: PathDict):
        return datum.node(self.source_path())


    def duration(self, datum: PathDict):
        schedule = datum.node(self.schedule_path())

        return int(schedule['interval']) * int(schedule['tally'])


    # ----------------------------------------------------------------------------------------------------------------

    def tag_path(self):
        return '.'.join([self.topic, 'tag'])


    def species_path(self):
        return '.'.join([self.topic, 'val', self.species])


    def source_path(self):
        return '.'.join([self.topic, 'src'])


    def schedule_path(self):
        return '.'.join(['status.val.sch', self.schedule])


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def species(self):
        return self.__species


    @property
    def schedule(self):
        return self.__schedule


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DatumMapping:{topic:%s, species:%s, schedule:%s}" % \
               (self.topic, self.species, self.schedule)
