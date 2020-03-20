"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note: The system_serial_number is independent of both dfe serial number and host serial number. It is typically
associated with the hostname. The combination vendor-id + model-id + system-sn must be universally unique.

example:
{"vendor-id": "scs", "model-id": "ap1", "model": "Alpha Pi Eng", "config": "V1", "system-sn": 6}
{"vendor-id": "SCS", "model-id": "BGB", "model": "Praxis", "config": "BGB", "system-sn": 406}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class SystemID(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "system_id.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        vendor_id = jdict.get('vendor-id')
        model_id = jdict.get('model-id')

        model_name = jdict.get('model')
        configuration = jdict.get('config')

        system_serial_number = jdict.get('system-sn')

        return SystemID(vendor_id, model_id, model_name, configuration, system_serial_number)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, vendor_id, model_id, model_name, configuration, system_serial_number):
        """
        Constructor
        """
        self.__vendor_id = vendor_id                # string (3 chars)
        self.__model_id = model_id                  # string (3 chars)

        self.__model_name = model_name              # string
        self.__configuration = configuration        # string

        self.__system_serial_number = system_serial_number        # string (by convention, int)


    # ----------------------------------------------------------------------------------------------------------------

    def type_label(self):
        if self.model_name is None or self.configuration is None:
            return None

        return self.model_name + '/' + self.configuration


    def box_label(self):
        if self.model_name is None or self.configuration is None or self.system_serial_number is None:
            return None

        box_system_serial_number = str(self.system_serial_number).rjust(6, '0')

        return self.model_name + '/' + self.configuration + ' ' + box_system_serial_number


    def topic_label(self):
        if self.model_name is None or self.system_serial_number is None:
            return None

        topic_model_name = self.model_name.replace(' ', '-').replace('.', '').lower()
        topic_system_serial_number = str(self.system_serial_number).rjust(6, '0')

        return topic_model_name + '-' + topic_system_serial_number


    def message_tag(self):
        if self.vendor_id is None or self.model_id is None or self.system_serial_number is None:
            return None

        tag_vendor_id = self.vendor_id.lower()
        tag_model_id = self.model_id.lower()

        return tag_vendor_id + '-' + tag_model_id + '-' + str(self.system_serial_number)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['vendor-id'] = self.vendor_id
        jdict['model-id'] = self.model_id

        jdict['model'] = self.model_name
        jdict['config'] = self.configuration

        jdict['system-sn'] = self.system_serial_number

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
    def system_serial_number(self):
        return self.__system_serial_number


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SystemID:{vendor_id:%s, model_id:%s, model_name:%s, configuration:%s, system_serial_number:%s}" % \
               (self.vendor_id, self.model_id, self.model_name, self.configuration, self.system_serial_number)
