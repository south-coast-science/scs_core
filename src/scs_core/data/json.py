"""
Created on 13 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import os

from abc import abstractmethod

from collections import OrderedDict

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class JSONable(object):
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

class PersistentJSONable(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls, host):
        filename = os.path.join(*cls.persistence_location(host))

        instance = cls.load_from_file(filename)
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


    def save_to_file(self, directory, file):
        # directory...
        Filesystem.mkdir(directory)

        # file...
        jstr = JSONify.dumps(self)

        f = open(os.path.join(directory, file), "w")
        f.write(jstr + '\n')
        f.close()


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
    def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
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
