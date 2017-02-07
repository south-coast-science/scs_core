"""
Created on 13 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from abc import abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class JSONable(object):
    """
    classdocs
    """

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
    def load_from_file(cls, filename):
        print("loading:%s" % filename)

        try:
            f = open(filename, "r")                 # cls.filename(host)
        except FileNotFoundError:
            return cls.construct_from_jdict(None)

        jstr = f.read().strip()
        f.close()

        print("got:%s" % jstr)

        jdict = json.loads(jstr)
        print("jdict:%s" % jdict)

        return cls.construct_from_jdict(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def filename(cls, name):
        pass


    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, filename):
        jstr = JSONify.dumps(self)

        f = open(filename, "w")                     # self.__class__.filename(host)
        f.write(jstr)
        f.close()


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def as_json(self):
        pass


# --------------------------------------------------------------------------------------------------------------------

class JSONify(json.JSONEncoder):
    """
    classdocs
    """

    @staticmethod
    def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None,
                indent=None, separators=None, default=None, sort_keys=False, **kw):

        handler = JSONify if cls is None else cls

        return json.dumps(obj, skipkeys, ensure_ascii, check_circular, allow_nan, handler,
                          indent, separators, default, sort_keys, **kw)


    # ----------------------------------------------------------------------------------------------------------------

    def default(self, obj):
        if isinstance(obj, JSONable):
            return obj.as_json()

        return json.JSONEncoder.default(self, obj)
