"""
Created on 9 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
[{"rec": "2024-01-10T11:55:45Z", "cause": "checksum error"}]
"""

from collections import OrderedDict

from scs_core.csv.csv_log import CSVLog

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class OPCErrorLogEntry(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))
        cause = jdict.get('cause')

        return cls(rec, cause)


    @classmethod
    def construct(cls, cause):
        return cls(LocalizedDatetime.now(), cause)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, cause):
        """
        Constructor
        """
        self.__rec = rec                                    # LocalizedDatetime
        self.__cause = cause                                # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec.as_iso8601()
        jdict['cause'] = self.cause

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def cause(self):
        return self.__cause


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCErrorLogEntry:{rec:%s, cause:%s}" % (self.rec, self.cause)


# --------------------------------------------------------------------------------------------------------------------

class OPCErrorLog(CSVLog):
    """
    classdocs
    """

    __FILENAME = "opc_error_log.csv"
    __MAX_ENTRIES = 5000                                # 180 KB

    @classmethod
    def persistence_location(cls):
        return cls.log_dir(), cls.__FILENAME


    @classmethod
    def max_permitted_entries(cls):
        return cls.__MAX_ENTRIES


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls([]) if skeleton else None

        entries = [OPCErrorLogEntry.construct_from_jdict(entry_jdict) for entry_jdict in jdict]

        return cls(entries)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, entries):
        """
        Constructor
        """
        super().__init__()

        self.__entries = entries                            # array of OPCErrorLogEntry


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.__entries


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def entries(self):
        return self.__entries


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCErrorLog:{entries:%s}" % Str.collection(self.entries)


# --------------------------------------------------------------------------------------------------------------------

class OPCErrorSummary(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        return cls(jdict)


    @classmethod
    def load(cls, manager):
        return cls(OPCErrorLog.rows(manager))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, entries):
        """
        Constructor
        """
        self.__entries = entries                                # int or None


    def __eq__(self, other):
        try:
            return self.entries == other.entries

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.entries


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def entries(self):
        return self.__entries


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCErrorSummary:{entries:%s}" % self.entries
