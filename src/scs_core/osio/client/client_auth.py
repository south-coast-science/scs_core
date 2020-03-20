"""
Created on 17 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"user_id": "southcoastscience-dev", "client-id": "5401", "client-password": "wtxSrs2e"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class ClientAuth(PersistentJSONable):
    """
    classdocs
    """

    MQTT_HOST =        "mqtt.opensensors.io"          # hard-coded URL

    MQTT_TIMEOUT =     20.0


    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "osio_client_auth.json"

    @classmethod
    def persistence_location(cls, host):
        return host.osio_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        user_id = jdict.get('user-id')

        client_id = jdict.get('client-id')
        client_password = jdict.get('client-password')

        return ClientAuth(user_id, client_id, client_password)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, user_id, client_id, client_password):
        """
        Constructor
        """
        self.__user_id = user_id                        # string

        self.__client_id = client_id                    # string
        self.__client_password = client_password        # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['user-id'] = self.user_id

        jdict['client-id'] = self.client_id
        jdict['client-password'] = self.client_password

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def user_id(self):
        return self.__user_id


    @property
    def client_id(self):
        return self.__client_id


    @property
    def client_password(self):
        return self.__client_password


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ClientAuth:{user_id:%s, client_id:%s, client_password:%s}" % \
                    (self.user_id, self.client_id, self.client_password)
