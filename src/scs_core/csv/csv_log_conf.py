"""
Created on 13 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"root-path": "/Volumes/SCS/data"}
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class CSVLogConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "csv_log_conf.json"

    @classmethod
    def filename(cls, host):
        return os.path.join(host.conf_dir(), cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        root_path = jdict.get('root-path')

        return CSVLogConf(root_path)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, root_path):
        """
        Constructor
        """
        super().__init__()

        self.__root_path = root_path


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['root-path'] = self.root_path

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def root_path(self):
        return self.__root_path


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogConf:{root_path:%s}" %  self.root_path
