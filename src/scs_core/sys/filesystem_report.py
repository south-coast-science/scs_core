"""
Created on 25 Nov 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"path": "/srv/removable_data_storage", "available": false, "on-root": null}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.sys.filesystem import Filesystem


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
            return cls(path, True, on_root)

        except FileNotFoundError:
            return cls(path, False, None)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        path = jdict.get('path')
        available = jdict.get('available')
        on_root = jdict.get('on-root')

        return cls(path, available, on_root)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, available, on_root):
        """
        Constructor
        """
        self.__path = path                          # String
        self.__available = available                # bool
        self.__on_root = on_root                    # bool


    def __eq__(self, other):
        try:
            return self.path == other.path and self.available == other.available and self.on_root == other.on_root

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


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['path'] = self.path
        jdict['available'] = self.available
        jdict['on-root'] = self.on_root

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "FilesystemReport:{path:%s, available:%s, on_root:%s}" % (self.path, self.available, self.on_root)
