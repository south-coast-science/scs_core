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
    def config(cls, name, verbose=False, level=logging.ERROR, stream=sys.stdout):
        cls.__NAME = name

        level = logging.INFO if verbose else level
        logging.basicConfig(format='%(name)s: %(message)s', level=level, stream=stream)


    @classmethod
    def getLogger(cls, name=None):
        logger_name = name if cls.__NAME is None else cls.__NAME

        return logging.getLogger(logger_name)
