"""
Created on 13 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import os
import time

from abc import ABC, abstractmethod
from collections import OrderedDict

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class JSONable(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def as_list(self, jlist):
        del jlist[:]                                    # empty the list

        for key, value in self.as_json().items():
            try:
                value = value.as_json()                 # TODO: recurse to construct a list
            except AttributeError:
                pass

            jlist.append((key, value))                  # append the key-value pairs of the dictionary


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def as_json(self):              # TODO: handle named parameters of JSONify.dumps(..)
        pass


# --------------------------------------------------------------------------------------------------------------------

class JSONReport(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls, filename):
        if not os.path.isfile(filename):
            return cls.construct_from_jdict(None)

        f = open(filename, 'r')
        jstr = f.readline()
        f.close()

        jdict = json.loads(jstr)

        return cls.construct_from_jdict(jdict)


    @classmethod
    def delete(cls, filename):
        if filename is None:
            return

        os.remove(filename)


    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, _):
        return JSONReport()


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, filename):
        if filename is None:
            return

        # data...
        jstr = JSONify.dumps(self)

        # file...
        tmp_filename = filename + '.' + str(int(time.time()))

        f = open(tmp_filename, 'w')
        f.write(jstr + '\n')
        f.close()

        # atomic operation...
        os.rename(tmp_filename, filename)


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def as_json(self):
        pass


# --------------------------------------------------------------------------------------------------------------------

class PersistentJSONable(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls, host):
        try:
            filename = os.path.join(*cls.persistence_location(host))
        except NotImplementedError:
            return None

        instance = cls.load_from_file(filename)

        if instance is not None:
            instance.__host = host

        return instance


    @classmethod
    def load_from_file(cls, filename):
        try:
            f = open(filename, "r")
        except FileNotFoundError:
            return cls.construct_from_jdict(None)

        jstr = f.read().strip()
        f.close()

        jdict = json.loads(jstr, object_pairs_hook=OrderedDict)

        return cls.construct_from_jdict(jdict)


    @classmethod
    def delete(cls, host):
        os.remove(os.path.join(*cls.persistence_location(host)))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def persistence_location(cls, _):
        return None, None


    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, _):
        return PersistentJSONable()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__host = None


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        self.__host = host

        self.save_to_file(*self.persistence_location(host))


    def save_to_file(self, directory, filename):
        # data...
        jstr = JSONify.dumps(self)

        # file...
        Filesystem.mkdir(directory)

        abs_filename = os.path.join(directory, filename)
        tmp_filename = abs_filename + '.' + str(int(time.time()))

        f = open(tmp_filename, "w")
        f.write(jstr + '\n')
        f.close()

        # atomic operation...
        os.rename(tmp_filename, abs_filename)


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def as_json(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def host(self):
        return self.__host


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        hostname = None if self.host is None else self.host.name()

        return "PersistentJSONable:{host:%s}" % hostname


# --------------------------------------------------------------------------------------------------------------------

class JSONify(json.JSONEncoder):
    """
    classdocs
    """

    @staticmethod
    def dumps(obj, skipkeys=False, ensure_ascii=False, check_circular=True,
              allow_nan=True, cls=None, indent=None, separators=None,
              default=None, sort_keys=False, **kw):

        handler = JSONify if cls is None else cls

        return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                          allow_nan=allow_nan, cls=handler, indent=indent, separators=separators,
                          default=default, sort_keys=sort_keys, **kw)


    # ----------------------------------------------------------------------------------------------------------------

    def default(self, obj):
        if isinstance(obj, JSONable):
            return obj.as_json()

        return json.JSONEncoder.default(self, obj)
