"""
Created on 13 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/42568262/how-to-encrypt-text-with-a-password-in-python
"""

import json
import os
import time

from abc import abstractmethod


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


# --------------------------------------------------------------------------------------------------------------------

class JSONable(object):
    """
    classdocs
    """

    _INDENT = 4

    # ----------------------------------------------------------------------------------------------------------------

    def as_list(self, jlist):
        del jlist[:]                                    # empty the list

        for key, value in self.as_json().items():
            try:
                value = value.as_json()
            except AttributeError:
                pass

            jlist.append((key, value))                  # append the key-value pairs of the dictionary


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def as_json(self, *args, **kwargs):
        pass


# --------------------------------------------------------------------------------------------------------------------

class JSONReport(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls, filename):
        if filename is None:
            return None

        if not os.path.isfile(filename):
            return cls.construct_from_jdict(None)

        with open(filename, 'r') as f:
            jstr = f.read()

        jdict = json.loads(jstr.strip())

        return cls.construct_from_jdict(jdict)


    @classmethod
    def delete(cls, filename):
        if filename is None:
            return

        os.remove(filename)


    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict):
        return JSONReport()


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, filename):
        if filename is None:
            return

        # data...
        jstr = JSONify.dumps(self, indent=self._INDENT)

        # file...
        tmp_filename = '.'.join((filename, str(int(time.time()))))

        try:
            with open(tmp_filename, 'w') as f:
                f.write(jstr + '\n')

        except FileNotFoundError:           # the containing directory does not exist (yet)
            return False

        # atomic operation...
        os.rename(tmp_filename, filename)

        return True


# --------------------------------------------------------------------------------------------------------------------

class AbstractPersistentJSONable(JSONable):
    """
    classdocs
    """

    __AWS_DIR =             "aws"                               # hard-coded rel path
    __CONF_DIR =            "conf"                              # hard-coded rel path
    __HUE_DIR =             "hue"                               # hard-coded rel path
    __OSIO_DIR =            "osio"                              # hard-coded rel path

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def save(self, manager):
        pass

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def aws_dir(cls):
        return cls.__AWS_DIR


    @classmethod
    def conf_dir(cls):
        return cls.__CONF_DIR


    @classmethod
    def hue_dir(cls):
        return cls.__HUE_DIR


    @classmethod
    def osio_dir(cls):
        return cls.__OSIO_DIR


# --------------------------------------------------------------------------------------------------------------------

class PersistentJSONable(AbstractPersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def exists(cls, manager):
        try:
            dirname, filename = cls.persistence_location()
        except NotImplementedError:
            return False

        return manager.exists(dirname, filename)


    @classmethod
    def load(cls, manager, encryption_key=None):
        try:
            dirname, filename = cls.persistence_location()
        except NotImplementedError:
            return None

        if not manager.exists(dirname, filename):
            return cls.construct_from_jdict(None)

        jstr = manager.load(dirname, filename, encryption_key=encryption_key)

        return cls.construct_from_jdict(json.loads(jstr))


    @classmethod
    def delete(cls, manager):
        try:
            dirname, filename = cls.persistence_location()
            manager.remove(dirname, filename)

        except NotImplementedError:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnusedLocal

    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict):
        return PersistentJSONable()


    # noinspection PyUnusedLocal

    @classmethod
    @abstractmethod
    def persistence_location(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, manager, encryption_key=None):
        dirname, filename = self.persistence_location()
        jstr = JSONify.dumps(self, indent=self._INDENT)

        manager.save(jstr, dirname, filename, encryption_key=encryption_key)


# --------------------------------------------------------------------------------------------------------------------

class MultiPersistentJSONable(AbstractPersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def exists(cls, manager, name=None):
        try:
            dirname, filename = cls.persistence_location(name)
        except NotImplementedError:
            return False

        return manager.exists(dirname, filename)


    @classmethod
    def load(cls, manager, name=None, encryption_key=None):
        try:
            dirname, filename = cls.persistence_location(name)
        except NotImplementedError:
            return None

        if not manager.exists(dirname, filename):
            return cls.construct_from_jdict(None, name=name)

        jstr = manager.load(dirname, filename, encryption_key=encryption_key)

        return cls.construct_from_jdict(json.loads(jstr), name=name)


    @classmethod
    def delete(cls, manager, name=None):
        try:
            dirname, filename = cls.persistence_location(name)
            manager.remove(dirname, filename)

        except NotImplementedError:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnusedLocal

    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict, name=None):
        return PersistentJSONable()


    # noinspection PyUnusedLocal

    @classmethod
    @abstractmethod
    def persistence_location(cls, name):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name):
        self.__name = name                                          # string


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, manager, encryption_key=None):
        dirname, filename = self.persistence_location(self.name)
        jstr = JSONify.dumps(self, indent=self._INDENT)

        manager.save(jstr, dirname, filename, encryption_key=encryption_key)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MultiPersistentJSONable:{name:%s}" % self.name
