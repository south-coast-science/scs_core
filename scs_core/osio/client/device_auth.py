"""
Created on 17 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:

"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# TODO: throughout, replace host-as-a-parameter with an abstract Host class?

# --------------------------------------------------------------------------------------------------------------------

class DeviceAuth(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "osio_device_auth.json"

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

        username = jdict.get('username')

        client_id = jdict.get('client-id')
        client_password = jdict.get('client-password')

        return DeviceAuth(username, client_id, client_password)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, client_id, client_password):
        """
        Constructor
        """
        self.__username = username                      # String

        self.__client_id = client_id                    # String
        self.__client_password = client_password        # String


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['username'] = self.username

        jdict['client-id'] = self.client_id
        jdict['client-password'] = self.client_password

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.__username


    @property
    def client_id(self):
        return self.__client_id


    @property
    def client_password(self):
        return self.__client_password


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceAuth:{username:%s, client_id:%s, client_password:%s}" % \
                    (self.username, self.client_id, self.client_password)
