"""
Created on 13 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"root-path": "/Volumes/SCS/data", "delete-oldest": true}
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class CSVLoggerConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "csv_logger_conf.json"

    @classmethod
    def filename(cls, host):
        return os.path.join(host.conf_dir(), cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        root_path = jdict.get('root-path')
        delete_oldest = jdict.get('delete-oldest')

        return CSVLoggerConf(root_path, delete_oldest)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, root_path, delete_oldest):
        """
        Constructor
        """
        super().__init__()

        self.__root_path = root_path                            # string
        self.__delete_oldest = bool(delete_oldest)              # bool


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['root-path'] = self.root_path
        jdict['delete-oldest'] = self.delete_oldest

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def root_path(self):
        return self.__root_path


    @property
    def delete_oldest(self):
        return self.__delete_oldest


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLoggerConf:{root_path:%s, delete_oldest:%s}" %  (self.root_path, self.delete_oldest)
