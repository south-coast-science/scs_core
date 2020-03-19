"""
Created on 13 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"root-path": "/home/pi/SCS/logs", "delete-oldest": true, "write-interval": 0}
"""

from collections import OrderedDict

from scs_core.csv.csv_log import CSVLog
from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class CSVLoggerConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "csv_logger_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        root_path = jdict.get('root-path')
        delete_oldest = jdict.get('delete-oldest')
        write_interval = jdict.get('write-interval')

        return CSVLoggerConf(root_path, delete_oldest, write_interval)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, root_path, delete_oldest, write_interval):
        """
        Constructor
        """
        self.__root_path = root_path                            # string
        self.__delete_oldest = bool(delete_oldest)              # bool
        self.__write_interval = int(write_interval)             # int


    # ----------------------------------------------------------------------------------------------------------------

    def csv_log(self, topic_subject, tag=None, timeline_start=None):
        return CSVLog(self.root_path, topic_subject, tag=tag, timeline_start=timeline_start)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['root-path'] = self.root_path
        jdict['delete-oldest'] = self.delete_oldest
        jdict['write-interval'] = self.write_interval

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def root_path(self):
        return self.__root_path


    @property
    def delete_oldest(self):
        return self.__delete_oldest


    @property
    def write_interval(self):
        return self.__write_interval


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLoggerConf:{root_path:%s, delete_oldest:%s, write_interval:%s}" %  \
               (self.root_path, self.delete_oldest, self.write_interval)
