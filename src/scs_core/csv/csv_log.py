"""
Created on 9 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/845058/how-to-get-the-line-count-of-a-large-file-cheaply-in-python
https://stackoverflow.com/questions/33626623/the-most-efficient-way-to-remove-first-n-elements-in-a-list
"""

from abc import ABC, abstractmethod
from collections import OrderedDict

from scs_core.csv.csv_reader import CSVReader
from scs_core.csv.csv_writer import CSVWriter

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable, JSONify, PersistentJSONable
from scs_core.data.str import Str

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class LogEntry(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))
        event = jdict.get('event')

        return cls(rec, event)


    @classmethod
    def construct(cls, event):
        return cls(LocalizedDatetime.now(), event)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, event):
        """
        Constructor
        """
        self.__rec = rec                                    # LocalizedDatetime
        self.__event = event                                # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec.as_iso8601()
        jdict['event'] = self.event

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def event(self):
        return self.__event


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LogEntry:{rec:%s, event:%s}" % (self.rec, self.event)


# --------------------------------------------------------------------------------------------------------------------

class CSVLog(PersistentJSONable, ABC):
    """
    classdocs
    """

    __TRIM_MARGIN =         0.2                             # 20%
    __LOG_DIR =             "log"                           # hard-coded rel path

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def log_dir(cls):
        return cls.__LOG_DIR


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def max_permitted_entries(cls):
        pass


    @classmethod
    @abstractmethod
    def construct_entry(cls, event):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def rows(cls, manager):
        if not cls.exists(manager):
            return None

        dirname, filename = cls.persistence_location()
        abs_filename = manager.abs_filename(dirname, filename)

        num_lines = sum(1 for _ in open(abs_filename))

        return 0 if not num_lines else num_lines - 1                # ignore CSV header row


    @classmethod
    def trim(cls, manager, max_entries):
        if not cls.exists(manager):
            return

        dirname, filename = cls.persistence_location()
        abs_filename = manager.abs_filename(dirname, filename)

        with open(abs_filename) as f:
            lines = f.readlines()

        excess = len(lines) - max_entries

        if excess < 1:
            return

        remove = excess + int(max_entries * cls.__TRIM_MARGIN)

        del lines[1:remove]

        with open(abs_filename, "w") as f:
            f.writelines(lines)


    @classmethod
    def load(cls, manager, encryption_key=None, skeleton=False):
        if not cls.exists(manager):
            return cls.construct_from_jdict(None, skeleton=skeleton)

        dirname, filename = cls.persistence_location()
        text, last_modified = manager.load(dirname, filename)

        reader = CSVReader(text.splitlines())
        jdict = [cls.loads(row) for row in reader.rows()]

        try:
            obj = cls.construct_from_jdict(jdict, skeleton=skeleton)
            obj._last_modified = last_modified
            return obj

        except (AttributeError, TypeError):
            return None


    @classmethod
    def save_event(cls, manager, event, trim=False):
        cls.__save_entries(manager, [cls.construct_entry(event)])

        if trim:
            cls.trim(manager, cls.max_permitted_entries())


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __save_entries(cls, manager, entries):
        dirname, filename = cls.persistence_location()
        abs_filename = manager.abs_filename(dirname, filename)

        Filesystem.mkdir(manager.abs_dirname(dirname))
        append = cls.exists(manager)

        writer = None

        try:
            writer = CSVWriter(filename=abs_filename, append=append)

            for entry in entries:
                writer.write(JSONify.dumps(entry))

        finally:
            if writer:
                writer.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, entries):
        """
        Constructor
        """
        super().__init__()

        self.__entries = entries                            # array of JSONable


    def __len__(self):
        return len(self.entries)


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, manager, encryption_key=None):
        self.__save_entries(manager, self.entries)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.__entries


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def entries(self):
        return self.__entries


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{entries:%s}" % Str.collection(self.entries)
