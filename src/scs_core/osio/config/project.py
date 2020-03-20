"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"location-path": "/orgs/southcoastscience-dev/test/loc/1", "device-path": "/orgs/southcoastscience-dev/test/device"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Project(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =                "osio_project.json"

    @classmethod
    def persistence_location(cls, host):
        return host.osio_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_channel(cls, channel):
        return channel in ('C', 'G', 'P', 'S', 'X')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, org_id, group, location_id):
        path_root = '/orgs/' + org_id + '/'

        location_path = path_root + group + '/loc/' + str(location_id)
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
            return self.climate_topic_path()

        if channel == 'G':
            return self.gases_topic_path()

        if channel == 'P':
            return self.particulates_topic_path()

        if channel == 'S':
            return self.status_topic_path(system_id)

        if channel == 'X':
            return self.control_topic_path(system_id)

        raise ValueError("channel_path: unrecognised channel: %s" % channel)


    # ----------------------------------------------------------------------------------------------------------------

    def climate_topic_path(self):
        return self.__location_path + '/climate'


    def gases_topic_path(self):
        return self.__location_path + '/gases'


    def particulates_topic_path(self):
        return self.__location_path + '/particulates'


    def status_topic_path(self, system_id):
        return '/'.join((self.__device_path, system_id.topic_label(), 'status'))


    def control_topic_path(self, system_id):
        return '/'.join((self.__device_path, system_id.topic_label(), 'control'))


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
