"""
Created on 9 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
[{"rec": "2024-01-10T11:55:45Z", "event": "checksum error"}]
"""

from scs_core.csv.csv_log import CSVLog, LogEntry

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class OPCErrorLog(CSVLog):
    """
    classdocs
    """

    __FILENAME = "opc_error_log.csv"
    __MAX_ENTRIES = 5000                                # ≈ 180 KB

    @classmethod
    def persistence_location(cls):
        return cls.log_dir(), cls.__FILENAME


    @classmethod
    def max_permitted_entries(cls):
        return cls.__MAX_ENTRIES


    @classmethod
    def construct_entry(cls, event):
        return LogEntry.construct(event)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls([]) if skeleton else None

        entries = [LogEntry.construct_from_jdict(entry_jdict) for entry_jdict in jdict]

        return cls(entries)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, entries):
        """
        Constructor
        """
        super().__init__(entries)


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
