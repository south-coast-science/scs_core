"""
Created on 3 Sep 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

found from the OPC firmware

example JSON:
{"serial": "177336702", "firmware": "OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS"}
"""

from collections import OrderedDict

from scs_core.data.json import MultiPersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class OPCVersion(MultiPersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "opc_version.json"

    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))

        return cls.conf_dir(), filename


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, name=None, skeleton=False):
        if not jdict:
            return None

        serial_no = jdict.get('serial')
        firmware = jdict.get('firmware')

        return cls(serial_no, firmware, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_no, firmware, name=None):
        """
        Constructor
        """
        super().__init__(name)

        self.__serial_no = serial_no                        # string
        self.__firmware = firmware                          # string


    def __eq__(self, other):                                # ignore name
        try:
            return self.serial_no == other.serial_no and self.firmware == other.firmware

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def serial_no(self):
        return self.__serial_no


    @property
    def firmware(self):
        return self.__firmware


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['serial'] = self.serial_no
        jdict['firmware'] = self.firmware

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCVersion:{name:%s, serial_no:%s, firmware:%s}" %  \
               (self.name, self.serial_no, self.firmware)
