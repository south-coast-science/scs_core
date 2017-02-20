"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class DeviceID(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_id.json"

    @classmethod
    def filename(cls, host):
        return host.SCS_CONF + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        model = jdict.get('model')
        configuration = jdict.get('config')
        serial_number = int(jdict.get('serial'))

        return DeviceID(model, configuration, serial_number)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, configuration, serial_number):
        """
        Constructor
        """
        self.__model = model                    # string
        self.__configuration = configuration    # string
        self.__serial_number = serial_number    # int


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    def type_label(self):
        return self.model + '/' + self.configuration


    def box_label(self):
        return self.model + '/' + self.configuration + ' ' + str(self.serial_number).zfill(6)


    def topic_label(self):
        return self.model.replace(' ', '-').replace('.', '').lower() + '-' + str(self.serial_number).zfill(6)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.model
        jdict['config'] = self.configuration
        jdict['serial'] = self.serial_number

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def configuration(self):
        return self.__configuration


    @property
    def serial_number(self):
        return self.__serial_number


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceID:{model:%s, configuration:%s, serial_number:%s}" % \
               (self.model, self.configuration, self.serial_number)
