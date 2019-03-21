"""
Created on 21 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Site information required for a device that may join the AirNow-I project

example JSON:
{"host": "sftp.airnowdata.org", "port": 22, "username": "UNEPdatauser", "password": "xxx",
"remote-path": "/UNEP/AQCSV"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class AirNowUploaderConf(PersistentJSONable):
    """
    classdocs
    """

    DEFAULT_PORT = 22

    __FILENAME = "airnow_uploader_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        host = jdict.get('host')
        port = jdict.get('port')

        username = jdict.get('username')
        password = jdict.get('password')

        remote_path = jdict.get('remote-path')

        return AirNowUploaderConf(host, port, username, password, remote_path)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, port, username, password, remote_path):
        """
        Constructor
        """
        super().__init__()

        self.__host = str(host)                             # string
        self.__port = int(port)                             # int

        self.__username = str(username)                     # string
        self.__password = str(password)                     # string

        self.__remote_path = remote_path                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['host'] = self.host
        jdict['port'] = self.port

        jdict['username'] = self.username
        jdict['password'] = self.password

        jdict['remote-path'] = self.remote_path

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def host(self):
        return self.__host


    @property
    def port(self):
        return self.__port


    @property
    def username(self):
        return self.__username


    @property
    def password(self):
        return self.__password


    @property
    def remote_path(self):
        return self.__remote_path


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AirNowUploaderConf:{host:%s, port:%s, username:%s, password:%s, remote_path:%s}" %  \
               (self.host, self.port, self.username, self.password, self.remote_path)
