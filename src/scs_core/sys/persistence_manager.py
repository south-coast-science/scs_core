"""
Created on 20 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import time
import tzlocal

from abc import ABC, abstractmethod

from scs_core.data.datetime import LocalizedDatetime
from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class PersistenceManager(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def list(self, container, dirname):
        pass


    @abstractmethod
    def exists(self, dirname, filename):
        pass


    @abstractmethod
    def load(self, dirname, filename, encryption_key=None):
        pass


    @abstractmethod
    def save(self, text, dirname, filename, encryption_key=None):
        pass


    @abstractmethod
    def remove(self, dirname, filename):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def scs_path(cls):
        pass


# --------------------------------------------------------------------------------------------------------------------

class FilesystemPersistenceManager(PersistenceManager, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def list(cls, container, dirname):
        abs_dirname = str(os.path.join(container, dirname))

        try:
            return sorted(os.listdir(abs_dirname))

        except FileNotFoundError:
            return []


    @classmethod
    def exists(cls, dirname, filename):
        abs_filename = cls.abs_filename(dirname, filename)

        return os.path.isfile(abs_filename)


    @classmethod
    def load(cls, dirname, filename, encryption_key=None):
        abs_filename = cls.abs_filename(dirname, filename)

        try:
            with open(abs_filename) as f:
                text = f.read()

            if encryption_key:
                from scs_core.data.crypt import Crypt               # late import
                jstr = Crypt.decrypt(encryption_key, text)
            else:
                jstr = text

        except FileNotFoundError:
            return None, None

        timestamp = int(os.path.getmtime(abs_filename))
        last_modified = LocalizedDatetime.construct_from_timestamp(timestamp, tz=tzlocal.get_localzone()).utc()

        return jstr, last_modified


    @classmethod
    def save(cls, text, dirname, filename, encryption_key=None):
        abs_dirname = cls.abs_dirname(dirname)
        abs_filename = cls.abs_filename(dirname, filename)

        # file...
        if filename:
            Filesystem.mkdir(abs_dirname)

        tmp_filename = '.'.join((abs_filename, str(int(time.time()))))

        if encryption_key:
            from scs_core.data.crypt import Crypt                   # late import
            saved_text = Crypt.encrypt(encryption_key, text)
        else:
            saved_text = text + '\n'

        with open(tmp_filename, "w") as f:
            f.write(saved_text)

        # atomic operation...
        os.rename(tmp_filename, abs_filename)


    @classmethod
    def remove(cls, dirname, filename):
        abs_filename = cls.abs_filename(dirname, filename)

        try:
            os.remove(abs_filename)
        except FileNotFoundError:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def abs_dirname(cls, dirname):
        return str(os.path.join(cls.scs_path(), dirname))


    @classmethod
    def abs_filename(cls, dirname, filename):
        return str(os.path.join(cls.scs_path(), dirname, filename))

