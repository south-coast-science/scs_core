"""
Created on 7 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"location-path": "southcoastscience-dev/test/loc/1", "device-path": "southcoastscience-dev/test/device"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Project(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =                "aws_project.json"

    @classmethod
    def persistence_location(cls, host):
        return host.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    CHANNELS =  ('C', 'G', 'P', 'S', 'X')

    @classmethod
    def is_valid_channel(cls, channel):
        return channel in cls.CHANNELS


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, organisation, group, location):
        path_root = organisation + '/'

        location_path = path_root + group + '/loc/' + str(location)
        device_path = path_root + group + '/device'

        return Project(location_path, device_path)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        location_path = jdict.get('location-path')
        device_path = jdict.get('device-path')

        return Project(location_path, device_path)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, location_path, device_path):
        """
        Constructor
        """
        self.__location_path = location_path          # string
        self.__device_path = device_path              # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['location-path'] = self.__location_path
        jdict['device-path'] = self.__device_path

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def channel_path(self, channel, system_id):
        if channel == 'C':
            return self.subject_path('climate', system_id)

        if channel == 'G':
            return self.subject_path('gases', system_id)

        if channel == 'P':
            return self.subject_path('particulates', system_id)

        if channel == 'S':
            return self.subject_path('status', system_id)

        if channel == 'X':
            return self.subject_path('control', system_id)

        raise ValueError(channel)


    def subject_path(self, subject, system_id):
        if subject == 'climate' or subject == 'gases' or subject == 'particulates':
            return '/'.join((self.__location_path, subject))

        if subject == 'status' or subject == 'control':
            return '/'.join((self.__device_path, system_id.topic_label(), subject))

        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def location_path(self):
        return self.__location_path


    @property
    def device_path(self):
        return self.__device_path


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Project:{location_path:%s, device_path:%s}" % (self.location_path, self.device_path)
