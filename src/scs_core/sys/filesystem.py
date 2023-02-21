"""
Created on 12 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example FilesystemReport JSON:
{"path": "/srv/removable_data_storage", "is-available": true, "on-root": true, "used": 69}
"""

import os

from collections import OrderedDict

from scs_core.data.json import JSONable


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

        return tuple(File.construct(path, name) for name in sorted(os.listdir(path)))


    @classmethod
    def is_on_root_filesystem(cls, path):
        ds_rp = os.path.realpath(path)

        return os.stat(ds_rp).st_dev == os.stat('/').st_dev                     # may raise FileNotFoundError


    @classmethod
    def percentage_used(cls, path):
        ds_rp = os.path.realpath(path)
        statvfs = os.statvfs(ds_rp)

        return round(100 - (100 * statvfs.f_bavail / statvfs.f_blocks), 1)      # may raise FileNotFoundError


# --------------------------------------------------------------------------------------------------------------------

class FilesystemReport(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, path):
        try:
            on_root = Filesystem.is_on_root_filesystem(path)
            used = int(round(Filesystem.percentage_used(path)))

            return cls(path, True, on_root, used)

        except FileNotFoundError:
            return cls(path, False, None, None)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        path = jdict.get('path')
        available = jdict.get('is-available')
        on_root = jdict.get('on-root')
        used = jdict.get('used')

        return cls(path, available, on_root, used)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, available, on_root, used):
        """
        Constructor
        """
        self.__path = path                          # String
        self.__available = available                # bool
        self.__on_root = on_root                    # bool
        self.__used = used                          # int percentage


    def __eq__(self, other):
        try:
            return self.path == other.path and self.available == other.available and \
                   self.on_root == other.on_root and self.used == other.used

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


    @property
    def available(self):
        return self.__available


    @property
    def on_root(self):
        return self.__on_root


    @property
    def used(self):
        return self.__used


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['path'] = self.path
        jdict['is-available'] = self.available
        jdict['on-root'] = self.on_root
        jdict['used'] = self.used

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "FilesystemReport:{path:%s, available:%s, on_root:%s, used:%s}" % \
               (self.path, self.available, self.on_root, self.used)


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
