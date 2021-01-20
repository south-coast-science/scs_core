#!/usr/bin/env python3

"""
Created on 20 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

# import logging

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------
# run...

Logging.config('my_script', verbose=True)
# Logging.config('my_script', level=logging.DEBUG)

logger = Logging.getLogger()
print(logger.name)
print("-")

logger.debug("debug")
logger.info("info")
logger.error("error")

