"""
Created on 13 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

import json

from abc import abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class JSONable(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def as_list(self, jlist):
        del jlist[:]                                    # empty the list

        for key_value in self.as_json().items():
            jlist.append(key_value)                     # append the key-value pairs of the dictionary


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def as_json(self):          # TODO: handle named parameters of JSONify.dumps(..)
        pass


# --------------------------------------------------------------------------------------------------------------------

class PersistentJSONable(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls, host):
        instance = cls.load_from_file(cls.filename(host))

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


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def filename(cls, host):
        pass


    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict):
        return PersistentJSONable()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__host = None


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        self.__host = host

        self.save_to_file(self.filename(host))


    def save_to_file(self, filename):
        jstr = JSONify.dumps(self)

        f = open(filename, "w")
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


    # @host.setter
    # def host(self, host):
    #     self.__host = host


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PersistentJSONable:{host:%s}" % self.host


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
