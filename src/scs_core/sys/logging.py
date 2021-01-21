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

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def config(cls, name, verbose=False, level=logging.ERROR, stream=sys.stderr):
        cls.__NAME = name

        level = logging.INFO if verbose else level
        logging.basicConfig(format='%(name)s: %(message)s', level=level, stream=stream)


    @classmethod
    def getLogger(cls, name=None):
        logger_name = cls.__NAME if cls.__NAME else name

        return logging.getLogger(logger_name)
