"""
Created on 13 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"root-path": "/home/pi/SCS/logs", "delete-oldest": true, "write-interval": 0}
"""

from collections import OrderedDict

from scs_core.csv.csv_log import CSVLog

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import PersistentJSONable

from scs_core.sys.filesystem import FilesystemReport


# --------------------------------------------------------------------------------------------------------------------

class CSVLoggerConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "csv_logger_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        root_path = jdict.get('root-path')
        delete_oldest = jdict.get('delete-oldest')
        write_interval = jdict.get('write-interval')
        retrospection_limit = LocalizedDatetime.construct_from_iso8601(jdict.get('retrospection-limit'))

        return CSVLoggerConf(root_path, delete_oldest, write_interval, retrospection_limit)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, root_path, delete_oldest, write_interval, retrospection_limit):
        """
        Constructor
        """
        super().__init__()

        self.__root_path = root_path                                # string
        self.__delete_oldest = bool(delete_oldest)                  # bool
        self.__write_interval = int(write_interval)                 # int
        self.__retrospection_limit = retrospection_limit            # LocalizedDatetime or None


    def __eq__(self, other):
        try:
            return self.root_path == other.root_path and self.delete_oldest == other.delete_oldest and \
                   self.write_interval == other.write_interval

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def csv_log(self, topic_subject, tag=None, timeline_start=None):
        return CSVLog(self.root_path, topic_subject, tag=tag, timeline_start=timeline_start)


    def filesystem_report(self):
        return FilesystemReport.construct(self.root_path)


    def retrospection_start(self, timeline_start):
        if self.retrospection_limit is None or timeline_start is None:
            return timeline_start

        if timeline_start < self.retrospection_limit:
            return self.retrospection_limit

        return timeline_start


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['root-path'] = self.root_path
        jdict['delete-oldest'] = self.delete_oldest
        jdict['write-interval'] = self.write_interval
        jdict['retrospection-limit'] = self.retrospection_limit

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


    @property
    def retrospection_limit(self):
        return self.__retrospection_limit


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLoggerConf:{root_path:%s, delete_oldest:%s, write_interval:%s, retrospection_limit:%s}" %  \
               (self.root_path, self.delete_oldest, self.write_interval, self.retrospection_limit)
