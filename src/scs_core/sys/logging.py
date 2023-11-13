"""
Created on 20 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://realpython.com/python-logging/
"""

import logging
import sys


# --------------------------------------------------------------------------------------------------------------------

class LoggingSpecification(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, level):
        """
        Constructor
        """
        self.__name = name                              # string
        self.__level = level                            # int or string


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def level(self):
        return self.__level


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LoggingSpecification:{name:%s, level:%s}" %   (self.name, self.level)


# --------------------------------------------------------------------------------------------------------------------

# noinspection PyPep8Naming
class Logging(object):
    """
    classdocs
    """

    __NAME = None
    __LEVEL = logging.NOTSET

    __MULTI_FORMAT = '%(name)s: %(message)s'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def config(cls, name, verbose=False, level=logging.ERROR, stream=sys.stderr):       # for CLU
        cls.__NAME = name
        cls.__LEVEL = logging.INFO if verbose else level

        logging.basicConfig(format=cls.__MULTI_FORMAT, level=cls.__LEVEL, stream=stream)


    @classmethod
    def replicate(cls, specification: LoggingSpecification, stream=sys.stderr):         # for child process
        cls.__NAME = specification.name
        cls.__LEVEL = specification.level

        logging.basicConfig(format=cls.__MULTI_FORMAT, level=cls.__LEVEL, stream=stream)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def getLogger(cls, name=None):
        logger_name = cls.__NAME if cls.__NAME else name

        return logging.getLogger(name=logger_name)


    @classmethod
    def debugging_on(cls):
        return cls.__LEVEL == logging.DEBUG


    @classmethod
    def specification(cls):
        return LoggingSpecification(cls.__NAME, cls.__LEVEL)


    @classmethod
    def level(cls):
        return cls.__LEVEL
