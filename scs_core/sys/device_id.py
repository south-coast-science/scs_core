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
        return host.conf_dir() + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        vendor_id = jdict.get('vendor-id')
        model_id = jdict.get('model-id')

        model_name = jdict.get('model')
        configuration = jdict.get('config')
        serial_number = jdict.get('serial')

        return DeviceID(vendor_id, model_id, model_name, configuration, serial_number)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, vendor_id, model_id, model_name, configuration, serial_number):
        """
        Constructor
        """
        self.__vendor_id = vendor_id                # string (3 chars)
        self.__model_id = model_id                  # string (3 chars)

        self.__model_name = model_name              # string
        self.__configuration = configuration        # string
        self.__serial_number = serial_number        # string (by convention, int)


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    def type_label(self):
        if self.model_name is None or self.configuration is None:
            return None

        return self.model_name + '/' + self.configuration


    def box_label(self):
        if self.model_name is None or self.configuration is None or self.serial_number is None:
            return None

        return self.model_name + '/' + self.configuration + ' ' + str(self.serial_number).rjust(6, '0')


    def topic_label(self):
        if self.model_name is None or self.serial_number is None:
            return None

        return self.model_name.replace(' ', '-').replace('.', '').lower() + '-' + str(self.serial_number).rjust(6, '0')


    def message_tag(self):      # TODO: add signature
        if self.vendor_id is None or self.model_id is None or self.serial_number is None:
            return None

        return self.vendor_id.lower() + '-' + self.model_id.lower() + '-' + str(self.serial_number)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['vendor-id'] = self.vendor_id
        jdict['model-id'] = self.model_id

        jdict['model'] = self.model_name
        jdict['config'] = self.configuration
        jdict['serial'] = self.serial_number

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def vendor_id(self):
        return self.__vendor_id


    @property
    def model_id(self):
        return self.__model_id


    @property
    def model_name(self):
        return self.__model_name


    @property
    def configuration(self):
        return self.__configuration


    @property
    def serial_number(self):
        return self.__serial_number


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceID:{vendor_id:%s, model_id:%s, model_name:%s, configuration:%s, serial_number:%s}" % \
               (self.vendor_id, self.model_id, self.model_name, self.configuration, self.serial_number)
