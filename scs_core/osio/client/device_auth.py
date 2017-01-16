"""
Created on 17 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:

"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class DeviceAuth(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "topic_client_auth.json"

    @classmethod
    def filename(cls, host):
        return host.SCS_OSIO + cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        username = jdict.get('username')

        device_id = jdict.get('device-id')
        device_password = jdict.get('device-password')

        return DeviceAuth(username, device_id, device_password)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, device_id, device_password):
        """
        Constructor
        """
        self.__username = username                      # String

        self.__device_id = device_id                    # String
        self.__device_password = device_password        # String


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['username'] = self.username

        jdict['device-id'] = self.device_id
        jdict['device-password'] = self.device_password

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.__username


    @property
    def device_id(self):
        return self.__device_id


    @property
    def device_password(self):
        return self.__device_password


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceAuth:{username:%s, device_id:%s, device_password:%s}" % \
                    (self.username, self.device_id, self.device_password)
