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

    __FILENAME = "aws_project.json"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    ENVIRONMENT_CHANNELS =  ('C', 'G', 'P')
    SYSTEM_CHANNELS =  ('S', 'X')

    CHANNELS = ENVIRONMENT_CHANNELS + SYSTEM_CHANNELS

    @classmethod
    def is_valid_channel(cls, channel):
        return channel in cls.CHANNELS


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, organisation, group, location):
        std_organisation = organisation.replace(' ', '-').lower()
        std_group = group.replace(' ', '-').lower()

        location_path = '/'.join((std_organisation, std_group, 'loc', str(location)))
        device_path = '/'.join((std_organisation, std_group, 'device'))

        return Project(location_path, device_path)


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
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
        super().__init__()

        self.__location_path = location_path          # string
        self.__device_path = device_path              # string


    def __eq__(self, other):
        try:
            return self.location_path == other.location_path and self.device_path == other.device_path

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['location-path'] = self.__location_path
        jdict['device-path'] = self.__device_path

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def environment_paths(self, system_id):
        return tuple(self.channel_path(channel, system_id) for channel in self.ENVIRONMENT_CHANNELS)


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
