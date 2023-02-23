"""
Created on 13 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

MappingTask example:
{"org": "south-coast-science-demo", "group": "brighton", "loc": 1, "topic": "particulates", "device": "praxis-000401",
"parameters": ["pm1", "pm2p5", "pm10"], "duration": 1, "checkpoint": "**:/01:00", "agency-code": "AAA",
"site-code": "123MM123456789", "pocs": {}, "upload-start": "2019-02-01T00:00:00Z", "upload-end": null}
"""

from ast import literal_eval

from collections import OrderedDict

from scs_core.aqcsv.connector.datum_mapping import DatumMapping

from scs_core.aqcsv.data.aqcsv_datetime import AQCSVDatetime
from scs_core.aqcsv.data.aqcsv_site import AQCSVSite

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable, PersistentJSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class AirNowMappingTaskList(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "airnow_mapping_tasks.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return AirNowMappingTaskList({}) if skeleton else None

        tasks = {literal_eval(key): MappingTask.construct_from_jdict(task) for key, task in jdict.get('tasks').items()}

        return AirNowMappingTaskList(tasks)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tasks):
        """
        Constructor
        """
        super().__init__()

        self.__tasks = tasks                                        # dictionary of task.pk: task


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

        jdict['tasks'] = {str(key): task for key, task in self.__tasks.items()}

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


    def set_upload_start(self, pk, upload_start):
        self.__tasks[pk].upload_start = upload_start


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AirNowMappingTaskList:{tasks:%s}" % Str.collection(self.__tasks)


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
        duration = jdict.get('duration')
        checkpoint = jdict.get('checkpoint')

        agency_code = jdict.get('agency-code')
        site_code = jdict.get('site-code')
        pocs = jdict.get('pocs')

        upload_start = LocalizedDatetime.construct_from_jdict(jdict.get('upload-start'))
        upload_end = LocalizedDatetime.construct_from_jdict(jdict.get('upload-end'))

        return MappingTask(org, group, loc, topic, device, parameters, duration, checkpoint,
                           agency_code, site_code, pocs, upload_start, upload_end)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, org, group, loc, topic, device, parameters, duration, checkpoint,
                 agency_code, site_code, pocs, upload_start, upload_end):
        """
        Constructor
        """
        self.__org = org                                    # string
        self.__group = group                                # string
        self.__loc = int(loc)                               # int
        self.__topic = topic                                # string

        self.__device = device                              # string
        self.__parameters = tuple(parameters)               # tuple of string
        self.__duration = int(duration)                     # int                       minutes
        self.__checkpoint = checkpoint                      # string

        self.__agency_code = agency_code                    # string
        self.__site_code = site_code                        # string
        self.__pocs = pocs                                  # dictionary of parameter: index

        self.__upload_start = upload_start                  # LocalizedDatetime
        self.__upload_end = upload_end                      # LocalizedDatetime


    def __eq__(self, other):
        try:
            return self.org == other.org and \
                   self.group == other.group and \
                   self.loc == other.loc and \
                   self.topic == other.topic and \
                   self.device == other.device and \
                   self.parameters == other.parameters and \
                   self.duration == other.duration and \
                   self.checkpoint == other.checkpoint and \
                   self.agency_code == other.agency_code and \
                   self.site_code == other.site_code and \
                   self.pocs == other.pocs and \
                   self.upload_start == other.upload_start and \
                   self.upload_end == other.upload_end

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
        jdict['duration'] = self.duration
        jdict['checkpoint'] = self.checkpoint

        jdict['agency-code'] = self.agency_code
        jdict['site-code'] = self.site_code
        jdict['pocs'] = self.pocs

        jdict['upload-start'] = self.upload_start
        jdict['upload-end'] = self.upload_end

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def environment_path(self):
        return '/'.join((self.org, self.group, 'loc', str(self.loc), self.topic))


    def status_path(self):
        return '/'.join((self.org, self.group, 'device', self.device, 'status'))


    def mappings(self):
        return tuple(DatumMapping(self.topic, species, self.site_code) for species in self.parameters)


    def file_prefix(self):
        dt = AQCSVDatetime(LocalizedDatetime.now().utc().datetime)
        site = AQCSVSite.construct_from_code(self.site_code)

        return dt.filename_prefix() + '_' + str(site.country_code)          # goal is YYYYMMDDhhmm_CCC.AAAAAAAAAA


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
    def duration(self):
        return self.__duration


    @property
    def agency_code(self):
        return self.__agency_code


    @property
    def site_code(self):
        return self.__site_code


    @property
    def pocs(self):
        return self.__pocs


    @property
    def upload_start(self):
        return self.__upload_start


    @property
    def upload_end(self):
        return self.__upload_end


    @upload_end.setter
    def upload_end(self, upload_end):
        self.__upload_end = upload_end


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MappingTask:{org:%s, group:%s, loc:%s, topic:%s, device:%s, parameters:%s, duration:%s, " \
               "checkpoint:%s, agency_code:%s, site_code:%s, pocs:%s, upload_start:%s, upload_end:%s}" % \
               (self.org, self.group, self.loc, self.topic, self.device, self.parameters, self.duration,
                self.checkpoint, self.agency_code, self.site_code, self.pocs, self.upload_start, self.upload_end)
