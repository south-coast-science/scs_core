"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"location-path": "/orgs/southcoastscience-dev/test/loc/1", "device-path": "/orgs/southcoastscience-dev/test/device"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# TODO: we need to map AFE configs to OSIO schemas

# --------------------------------------------------------------------------------------------------------------------

class Publication(PersistentJSONable):
    """
    classdocs
    """

    CLIMATE_NAME =              "Climate"
    CLIMATE_DESCRIPTION =       "temperature (Centigrade), relative humidity (%)"
    CLIMATE_SCHEMA =            None                                            # TODO: needs a schema

    GASES_NAME =                "Gas concentrations"
    GASES_DESCRIPTION =         "electrochemical we (V), ae (V), wc (V), cnc (ppb), Pt100 temp, internal SHT"
    GASES_SCHEMA =              28                                              # TODO: should come from AFEConfig

    PARTICULATES_NAME =         "Particulate densities"
    PARTICULATES_DESCRIPTION =  "pm1 (ug/m3), pm2.5 (ug/m3), pm10 (ug/m3), bin counts, mtf1, mtf3, mtf5 mtf7"
    PARTICULATES_SCHEMA =       29

    STATUS_NAME =               "Device status"
    STATUS_DESCRIPTION =        "lat (deg), lng (deg) GPS qual, DFE temp (Centigrade), host temp (Centigrade), errors"
    STATUS_SCHEMA =             None                                            # TODO: needs a schema

    CONTROL_NAME =              "Device control"
    CONTROL_DESCRIPTION =       "this topic is subscribed to by the device"
    CONTROL_SCHEMA =            None


    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =                "osio_publication.json"

    @classmethod
    def filename(cls, host):
        return host.SCS_OSIO + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, org_id, group, location_id):
        path_root = '/orgs/' + org_id + '/'

        location_path = path_root + group + '/loc/' + str(location_id)
        device_path = path_root + group + '/device'

        return Publication(location_path, device_path)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        location_path = jdict.get('location-path')
        device_path = jdict.get('device-path')

        return Publication(location_path, device_path)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, location_path, device_path):
        """
        Constructor
        """
        self.__location_path = location_path          # string
        self.__device_path = device_path              # string


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['location-path'] = self.__location_path
        jdict['device-path'] = self.__device_path

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def climate_topic_path(self):
        return self.__location_path + '/climate'


    def gases_topic_path(self):
        return self.__location_path + '/gases'


    def particulates_topic_path(self):
        return self.__location_path + '/particulates'


    def status_topic_path(self, device_id):
        return self.__device_path + '/' + device_id.topic_label() + '/status'


    def control_topic_path(self, device_id):
        return self.__device_path + '/' + device_id.topic_label() + '/control'


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def location_path(self):
        return self.__location_path


    @property
    def device_path(self):
        return self.__device_path


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Publication:{location_path:%s, device_path:%s}" % (self.location_path, self.device_path)
