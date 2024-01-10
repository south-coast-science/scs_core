"""
Created on 9 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod

from scs_core.csv.csv_reader import CSVReader
from scs_core.csv.csv_writer import CSVWriter

from scs_core.data.json import JSONify, PersistentJSONable

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class CSVLog(PersistentJSONable, ABC):
    """
    classdocs
    """

    __LOG_DIR =             "log"                               # hard-coded rel path

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def log_dir(cls):
        return cls.__LOG_DIR


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def max_permitted_entries(cls):
        return None


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

        remove = len(lines) - max_entries

        if remove < 1:
            return

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
    def save_entry(cls, manager, entry, trim=False):
        cls.__save_entries(manager, [entry])

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

    def __len__(self):
        return len(self.entries)


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, manager, encryption_key=None):
        self.__save_entries(manager, self.entries)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def entries(self):
        return []
