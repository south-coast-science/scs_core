"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Publication(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "osio_publication.json"

    @classmethod
    def filename(cls, host):
        return host.SCS_OSIO + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        location_path_root = jdict.get('location-path-root')
        device_path_root = jdict.get('device-path-root')

        return Publication(location_path_root, device_path_root)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, location_path_root, device_path_root):
        """
        Constructor
        """
        self.__location_path_root = location_path_root          # string
        self.__device_path_root = device_path_root              # string


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['location-path-root'] = self.__location_path_root
        jdict['device-path-root'] = self.__device_path_root

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def gasses_topic(self):
        return self.__location_path_root + '/gasses'


    @property
    def particulates_topic(self):
        return self.__location_path_root + '/particulates'


    @property
    def climate_topic(self):
        return self.__location_path_root + '/climate'


    @property
    def status_topic(self):
        return self.__device_path_root + '/status'             # TODO: need to get the device ID!


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Publication:{location_path_root:%s, device_path_root:%s}" % \
               (self.__location_path_root, self.__device_path_root)
