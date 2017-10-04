"""
Created on 4 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"name": "rpi-006", "certificate": "9f01402232"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class ClientID(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "client_id.json"

    @classmethod
    def filename(cls, host):
        return host.aws_dir() + cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    __CERTIFICATE_DIR = "certs/"

    __ROOT_CA = "root-CA.crt"

    __PUBLIC_KEY_SUFFIX = "-public.pem.key"
    __PRIVATE_KEY_SUFFIX = "-private.pem.key"
    __CERTIFICATE_SUFFIX = "-certificate.pem.crt"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        name = jdict.get('name')
        certificate = jdict.get('certificate')

        return ClientID(name, certificate)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, certificate):
        """
        Constructor
        """
        super().__init__()

        self.__name = name                          # String
        self.__certificate = certificate            # String


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['name'] = self.name
        jdict['certificate'] = self.certificate

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def root_ca_file_path(self):
        return self.host.aws_dir() + self.__CERTIFICATE_DIR + self.__ROOT_CA


    @property
    def certificate_path(self):
        return self.host.aws_dir() + self.__CERTIFICATE_DIR + self.certificate + self.__CERTIFICATE_SUFFIX


    @property
    def public_key_path(self):
        return self.host.aws_dir() + self.__CERTIFICATE_DIR + self.certificate + self.__PUBLIC_KEY_SUFFIX


    @property
    def private_key_path(self):
        return self.host.aws_dir() + self.__CERTIFICATE_DIR + self.certificate + self.__PRIVATE_KEY_SUFFIX


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def certificate(self):
        return self.__certificate


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ClientID:{host:%s, name:%s, certificate:%s}" % (self.host, self.name, self.certificate)
