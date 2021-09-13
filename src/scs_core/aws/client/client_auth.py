"""
Created on 2 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

WARNING: Path methods require that the __HOST field must be instantiated.

example document:
{"endpoint": "endpoint.iot.us-west-2.amazonaws.com", "client-id": "bruno", "cert-id": "9f08402232"}
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class ClientAuth(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "aws_client_auth.json"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    @classmethod
    def load(cls, manager, encryption_key=None, skeleton=False):
        auth = super().load(manager, encryption_key=encryption_key, skeleton=skeleton)

        if auth is None:
            return None

        auth.manager = manager

        return auth


    # ----------------------------------------------------------------------------------------------------------------

    __CERT_DIR = "certs"                                # hard-coded path

    __ROOT_CA = "root-CA.crt"

    __PUBLIC_KEY_SUFFIX = "-public.pem.key"
    __PRIVATE_KEY_SUFFIX = "-private.pem.key"
    __CERT_SUFFIX = "-certificate.pem.crt"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        endpoint = jdict.get('endpoint')
        client_id = jdict.get('client-id')
        cert_id = jdict.get('cert-id')

        return ClientAuth(endpoint, client_id, cert_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, endpoint, client_id, cert_id, manager=None):
        """
        Constructor
        """
        super().__init__()

        self.__endpoint = endpoint                  # String
        self.__client_id = client_id                # String
        self.__cert_id = cert_id                    # String

        self.__manager = manager                    # FilesystemPersistenceManager


    def __eq__(self, other):                # ignore manager
        try:
            return self.endpoint == other.endpoint and self.client_id == other.client_id and \
                   self.cert_id == other.cert_id

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['endpoint'] = self.endpoint
        jdict['client-id'] = self.client_id
        jdict['cert-id'] = self.cert_id

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def installed_ok(self):
        if not os.access(self.root_ca_file_path, os.R_OK):
            return False

        if not os.access(self.certificate_path, os.R_OK):
            return False

        if not os.access(self.public_key_path, os.R_OK):
            return False

        if not os.access(self.private_key_path, os.R_OK):
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def root_ca_file_path(self):
        return os.path.join(self.__cert_path(), self.__ROOT_CA)


    @property
    def certificate_path(self):
        return os.path.join(self.__cert_path(), self.cert_id + self.__CERT_SUFFIX)


    @property
    def public_key_path(self):
        return os.path.join(self.__cert_path(), self.cert_id + self.__PUBLIC_KEY_SUFFIX)


    @property
    def private_key_path(self):
        return os.path.join(self.__cert_path(), self.cert_id + self.__PRIVATE_KEY_SUFFIX)


    # ----------------------------------------------------------------------------------------------------------------

    def __cert_path(self):
        return os.path.join(self.manager.scs_path(), self.aws_dir(), self.__CERT_DIR)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def endpoint(self):
        return self.__endpoint


    @property
    def client_id(self):
        return self.__client_id


    @property
    def cert_id(self):
        return self.__cert_id


    @property
    def manager(self):
        return self.__manager


    @manager.setter
    def manager(self, manager):
        self.__manager = manager


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ClientAuth:{endpoint:%s, client_id:%s, cert_id:%s, manager:%s}" % \
               (self.endpoint, self.client_id, self.cert_id, self.manager)
