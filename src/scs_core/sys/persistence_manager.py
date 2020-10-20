"""
Created on 20 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import time

from abc import ABC, abstractmethod

from scs_core.data.crypt import Crypt
from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class PersistenceManager(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def exists(self, dirname, filename):
        pass


    @abstractmethod
    def load(self, dirname, filename, encryption_key=None):
        pass


    @abstractmethod
    def save(self, jstr, dirname, filename, encryption_key=None):
        pass


    @abstractmethod
    def remove(self, dirname, filename):
        pass


# --------------------------------------------------------------------------------------------------------------------

class FilesystemPersistenceManager(PersistenceManager):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def exists(self, dirname, filename):
        abs_filename = self.__abs_filename(dirname, filename)

        return os.path.isfile(abs_filename)


    def load(self, dirname, filename, encryption_key=None):
        abs_filename = self.__abs_filename(dirname, filename)

        try:
            with open(abs_filename, "r") as f:
                text = f.read()

            jstr = text if encryption_key is None else Crypt.decrypt(encryption_key, text)

        except FileNotFoundError:
            return None

        return jstr


    def save(self, jstr, dirname, filename, encryption_key=None):
        abs_dirname = self.__abs_dirname(dirname)
        abs_filename = self.__abs_filename(dirname, filename)

        # file...
        if filename:
            Filesystem.mkdir(abs_dirname)

        tmp_filename = '.'.join((abs_filename, str(int(time.time()))))

        text = jstr + '\n' if encryption_key is None else Crypt.encrypt(encryption_key, jstr)

        with open(tmp_filename, "w") as f:
            f.write(text)

        # atomic operation...
        os.rename(tmp_filename, abs_filename)


    def remove(self, dirname, filename):
        abs_filename = self.__abs_filename(dirname, filename)

        try:
            os.remove(abs_filename)
        except FileNotFoundError:
            pass

    # ----------------------------------------------------------------------------------------------------------------

    def __abs_filename(self, dirname, filename):
        return os.path.join(self.scs_path(), dirname, filename)


    def __abs_dirname(self, dirname):
        return os.path.join(self.scs_path(), dirname)


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def scs_path(self):
        pass
