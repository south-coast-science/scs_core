"""
Created on 21 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Site information required for a device that may join the AirNow-I project

example JSON:
{"host": "sftp.airnowdata.org", "port": 22, "username": "UNEPdatauser", "password": "xxx",
"remote-path": "/UNEP/AQCSV"}
"""

from scs_core.client.sftp_client_conf import SFTPClientConf

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class AirNowUploaderConf(SFTPClientConf, PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "airnow_uploader_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, port, username, password, remote_path):
        super().__init__(host, port, username, password, remote_path)
