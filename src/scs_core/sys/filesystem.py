"""
Created on 12 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os


# --------------------------------------------------------------------------------------------------------------------

class Filesystem(object):

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def mkdir(cls, path):
        if not path or os.path.exists(path):
            return

        head, _ = os.path.split(path)

        if head and not os.path.exists(head):
            cls.mkdir(head)

        if not os.path.exists(path):                # handles case of trailing /
            try:
                os.mkdir(path)
            except FileExistsError:
                raise FileNotFoundError(path)       # covers a Python bug


    @classmethod
    def rmdir(cls, path):
        if not path or not os.path.exists(path):
            return False

        try:
            os.rmdir(path)
            return True

        except OSError:
            return False


    @classmethod
    def rm(cls, path):
        if not path or not os.path.exists(path):
            return False

        try:
            os.remove(path)
            return True

        except OSError:
            return False


    @classmethod
    def ls(cls, path):
        if not path or not os.path.exists(path):
            return None

        return (File.construct(path, name) for name in sorted(os.listdir(path)))


# --------------------------------------------------------------------------------------------------------------------

class File(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, container, name):
        abs_filename = os.path.join(container, name)

        return File(container, name, os.path.getmtime(abs_filename), os.path.isdir(abs_filename))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, container, name, updated, is_directory):
        """
        Constructor
        """
        self.__container = container                            # string
        self.__name = name                                      # string
        self.__updated = int(updated)                           # int timestamp
        self.__is_directory = bool(is_directory)                # bool


    # ----------------------------------------------------------------------------------------------------------------

    def path(self):
        return os.path.join(self.container, self.name)


    def has_suffix(self, suffix):
        return self.name.endswith('.' + suffix)


    def delete(self):
        return Filesystem.rm(self.path())


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def container(self):
        return self.__container


    @property
    def name(self):
        return self.__name


    @property
    def updated(self):
        return self.__updated


    @property
    def is_directory(self):
        return self.__is_directory


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "File:{container:%s, name:%s, updated:%s, is_directory:%s}" %  \
               (self.container, self.name, self.updated, self.is_directory)
