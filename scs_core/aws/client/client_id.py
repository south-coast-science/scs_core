"""
Created on 4 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"id": "rpi-006", "certificate": "9f01402232"}

# rootCAPath = "/home/pi/SCS/aws/root-CA.crt"
# certificatePath = "/home/pi/SCS/aws/scs-rpi-006.cert.pem"  # 9f01402232-certificate.pem.crt
# privateKeyPath = "/home/pi/SCS/aws/scs-rpi-006.private.key"  # 9f01402232-private.pem.key

def configureCredentials(self, CAFilePath, KeyPath="", CertificatePath=""):  # Should be good for MutualAuth certs config and Websocket rootCA config
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


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    __CERTIFICATE_DIR = "certs/"

    __ROOT_CA = "root-CA.crt"

    __PUBLIC_KEY_SUFFIX = "-public.pem.key"
    __PRIVATE_KEY_SUFFIX = "-private.pem.key"
    __CERTIFICATE_SUFFIX = "-certificate.pem.crt"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def root_ca_file_path(cls, host):
        return host.aws_dir() + cls.__CERTIFICATE_DIR + cls.__ROOT_CA



    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        name = jdict.get('id')
        certificate = jdict.get('certificate')

        return ClientID(name, certificate)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, certificate):
        """
        Constructor
        """
        self.__id = id                              # String
        self.__certificate = certificate            # String


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['id'] = self.id
        jdict['certificate'] = self.certificate

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def certificate_path(self, host):
        return host.aws_dir() + self.__CERTIFICATE_DIR + self.certificate + self.__CERTIFICATE_SUFFIX


    def public_key_path(self, host):
        return host.aws_dir() + self.__CERTIFICATE_DIR + self.certificate + self.__PUBLIC_KEY_SUFFIX


    def private_key_path(self, host):
        return host.aws_dir() + self.__CERTIFICATE_DIR + self.certificate + self.__PRIVATE_KEY_SUFFIX


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def certificate(self):
        return self.__certificate


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ClientID:{id:%s, certificate:%s}" % (self.id, self.certificate)
