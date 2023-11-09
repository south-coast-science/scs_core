"""
Created on 20 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://realpython.com/python-logging/
"""

import logging
import sys


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
    def config(cls, name, verbose=False, level=logging.ERROR, stream=sys.stderr):
        cls.__NAME = name
        cls.__LEVEL = logging.INFO if verbose else level

        logging.basicConfig(format=cls.__MULTI_FORMAT, level=cls.__LEVEL, stream=stream)


    @classmethod
    def getLogger(cls, name=None):
        logger_name = cls.__NAME if cls.__NAME else name

        return logging.getLogger(name=logger_name)


    @classmethod
    def name(cls):
        return cls.__NAME


    @classmethod
    def level(cls):
        return cls.__LEVEL


    @classmethod
    def debugging_on(cls):
        return cls.__LEVEL == logging.DEBUG
