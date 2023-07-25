"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note: The system_serial_number is independent of both dfe serial number and host serial number. It is typically
associated with the hostname. The combination vendor-id + model-id + system-sn must be universally unique.

examples:
{"vendor-id": "scs", "model-id": "ap1", "model": "Alpha Pi Eng", "config": "V1", "system-sn": 6}
{"vendor-id": "SCS", "model-id": "BGB", "model": "Praxis", "config": "BGB", "system-sn": 406}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class SystemID(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "system_id.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        last_modified = LocalizedDatetime.construct_from_jdict(jdict.get('set-on'))

        vendor_id = jdict.get('vendor-id')
        model_id = jdict.get('model-id')

        model_name = jdict.get('model')
        configuration = jdict.get('config')

        system_serial_number = jdict.get('system-sn')

        return SystemID(vendor_id, model_id, model_name, configuration, system_serial_number,
                        last_modified=last_modified)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, vendor_id, model_id, model_name, configuration, system_serial_number,
                 last_modified=None):
        """
        Constructor
        """
        super().__init__(last_modified=last_modified)

        self.__vendor_id = vendor_id                                # string (3 chars)
        self.__model_id = model_id                                  # string (3 chars)

        self.__model_name = model_name                              # string
        self.__configuration = configuration                        # string

        self.__system_serial_number = system_serial_number          # string (by convention, int)


    def __eq__(self, other):
        try:
            return bool(self.last_modified) == bool(other.last_modified) and \
                   self.vendor_id == other.vendor_id and self.model_id == other.model_id and \
                   self.model_name == other.model_name and self.configuration == other.configuration and \
                   self.system_serial_number == other.system_serial_number

        except (TypeError, AttributeError):
            return False


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

        topic_model_name = self.model_name.replace('/', '-').replace(' ', '-').replace('.', '').lower()
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

        if self.last_modified:
            jdict['set-on'] = None if self.last_modified is None else self.last_modified.as_iso8601()

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


    @system_serial_number.setter
    def system_serial_number(self, system_serial_number):
        self.__system_serial_number = system_serial_number


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SystemID:{vendor_id:%s, model_id:%s, model_name:%s, configuration:%s, system_serial_number:%s}" % \
               (self.vendor_id, self.model_id, self.model_name, self.configuration, self.system_serial_number)
