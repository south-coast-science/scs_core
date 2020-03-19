"""
Created on 2 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

WARNING: Path methods require that the __HOST field must be instantiated.

example document:
{"endpoint": "asrft7e5j5ecz.iot.us-west-2.amazonaws.com", "client-id": "bruno", "cert-id": "9f08402232"}
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
    __HOST = None


    @classmethod
    def persistence_location(cls, host):
        cls.__HOST = host

        return host.aws_dir(), cls.__FILENAME


    @classmethod
    def set_host(cls, host):
        cls.__HOST = host


    # ----------------------------------------------------------------------------------------------------------------

    __CERT_DIR = "certs"                                # hard-coded path

    __ROOT_CA = "root-CA.crt"

    __PUBLIC_KEY_SUFFIX = "-public.pem.key"
    __PRIVATE_KEY_SUFFIX = "-private.pem.key"
    __CERT_SUFFIX = "-certificate.pem.crt"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        endpoint = jdict.get('endpoint')
        client_id = jdict.get('client-id')
        cert_id = jdict.get('cert-id')

        return ClientAuth(endpoint, client_id, cert_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, endpoint, client_id, cert_id):
        """
        Constructor
        """
        self.__endpoint = endpoint                  # String
        self.__client_id = client_id                # String
        self.__cert_id = cert_id                    # String


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
        return os.path.join(self.__HOST.aws_dir(), self.__CERT_DIR, self.__ROOT_CA)


    @property
    def certificate_path(self):
        return os.path.join(self.__HOST.aws_dir(), self.__CERT_DIR, self.cert_id + self.__CERT_SUFFIX)


    @property
    def public_key_path(self):
        return os.path.join(self.__HOST.aws_dir(), self.__CERT_DIR, self.cert_id + self.__PUBLIC_KEY_SUFFIX)


    @property
    def private_key_path(self):
        return os.path.join(self.__HOST.aws_dir(), self.__CERT_DIR, self.cert_id + self.__PRIVATE_KEY_SUFFIX)


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


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ClientAuth:{endpoint:%s, client_id:%s, cert_id:%s}" % (self.endpoint, self.client_id, self.cert_id)
