"""
Created on 13 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

MappingTask example:
{"org": "south-coast-science-demo", "group": "brighton", "loc": 1, "topic": "particulates", "device": "praxis-000401",
"parameters": ["val.pm1", "val.pm2p5", "val.pm10"], "checkpoint": "**:/01:00", "site-code": "123MM123456789",
"pocs": {"88101": 2, "85101": 3}, "latest-rec": "2019-03-13T12:45:00Z"}
"""

from ast import literal_eval

from collections import OrderedDict

from scs_core.aqcsv.connector.datum_mapping import DatumMapping

from scs_core.data.json import JSONable, PersistentJSONable
from scs_core.data.localized_datetime import LocalizedDatetime


# TODO: add agency code to MappingTask

# --------------------------------------------------------------------------------------------------------------------

class AirNowMappingTaskList(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "airnow_mapping_tasks.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return AirNowMappingTaskList({})

        tasks = {literal_eval(key): MappingTask.construct_from_jdict(task) for key, task in jdict.get('tasks').items()}

        return AirNowMappingTaskList(tasks)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tasks):
        """
        Constructor
        """
        super().__init__()

        self.__tasks = tasks                                    # dictionary of task.pk: task


    # ----------------------------------------------------------------------------------------------------------------

    def items(self):
        return self.__tasks.values()


    def item(self, pk):
        if pk not in self.__tasks:
            return None

        return self.__tasks[pk]


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tasks'] = {str(key): task for key, task in self.tasks.items()}

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def insert(self, task):
        self.__tasks[task.pk] = task

        # sort...
        tasks = OrderedDict()

        for pk in sorted(self.__tasks.keys()):
            tasks[pk] = self.__tasks[pk]

        self.__tasks = tasks


    def remove(self, pk):
        try:
            del(self.__tasks[pk])

        except KeyError:
            pass


    def set_latest_rec(self, pk, latest_rec):
        self.__tasks[pk].latest_rec = latest_rec


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tasks(self):
        return self.__tasks


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        tasks = '{' + ', '.join(str(key) + ': ' + str(self.tasks[key]) for key in self.tasks) + '}'

        return "AirNowMappingTaskList:{tasks:%s}" % tasks


# --------------------------------------------------------------------------------------------------------------------

class MappingTask(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        org = jdict.get('org')
        group = jdict.get('group')
        loc = jdict.get('loc')
        topic = jdict.get('topic')

        device = jdict.get('device')
        parameters = jdict.get('parameters')
        checkpoint = jdict.get('checkpoint')

        site_code = jdict.get('site-code')
        pocs = jdict.get('pocs')

        latest_rec = LocalizedDatetime.construct_from_jdict(jdict.get('latest-rec'))

        return MappingTask(org, group, loc, topic, device, parameters, checkpoint, site_code, pocs, latest_rec)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, org, group, loc, topic, device, parameters, checkpoint, site_code, pocs, latest_rec):
        """
        Constructor
        """
        self.__org = org                                    # string
        self.__group = group                                # string
        self.__loc = int(loc)                               # int
        self.__topic = topic                                # string

        self.__device = device                              # string
        self.__parameters = tuple(parameters)               # tuple of string
        self.__checkpoint = checkpoint                      # string

        self.__site_code = site_code                        # string
        self.__pocs = pocs                                  # dictionary of parameter: index

        self.__latest_rec = latest_rec                      # LocalizedDatetime


    def __eq__(self, other):
        try:
            return self.org == other.org and \
                   self.group == other.group and \
                   self.loc == other.loc and \
                   self.topic == other.topic and \
                   self.device == other.device and \
                   self.parameters == other.parameters and \
                   self.checkpoint == other.checkpoint and \
                   self.site_code == other.site_code and \
                   self.pocs == other.pocs and \
                   self.latest_rec == other.latest_rec

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['org'] = self.org
        jdict['group'] = self.group
        jdict['loc'] = self.loc
        jdict['topic'] = self.topic

        jdict['device'] = self.device
        jdict['parameters'] = self.parameters
        jdict['checkpoint'] = self.checkpoint

        jdict['site-code'] = self.site_code
        jdict['pocs'] = self.pocs

        jdict['latest-rec'] = self.latest_rec

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def environment_path(self):
        return '/'.join((self.org, self.group, 'loc', str(self.loc), self.topic))


    def status_path(self):
        return '/'.join((self.org, self.group, 'device', self.device, 'status'))


    def mappings(self):
        return (DatumMapping(self.topic, species, self.site_code) for species in self.parameters)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pk(self):
        return self.org, self.group, self.loc, self.topic


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def org(self):
        return self.__org


    @property
    def group(self):
        return self.__group


    @property
    def loc(self):
        return self.__loc


    @property
    def topic(self):
        return self.__topic


    @property
    def device(self):
        return self.__device


    @property
    def parameters(self):
        return self.__parameters


    @property
    def checkpoint(self):
        return self.__checkpoint


    @property
    def site_code(self):
        return self.__site_code


    @property
    def pocs(self):
        return self.__pocs


    @property
    def latest_rec(self):
        return self.__latest_rec


    @latest_rec.setter
    def latest_rec(self, latest_rec):
        self.__latest_rec = latest_rec


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MappingTask:{org:%s, group:%s, loc:%s, topic:%s, device:%s, parameters:%s, checkpoint:%s, " \
               "site_code:%s, pocs:%s, latest_rec:%s}" % \
               (self.org, self.group, self.loc, self.topic, self.device, self.parameters, self.checkpoint,
                self.site_code, self.pocs, self.latest_rec)
