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
# print(logger.name)
print("-")

logger.error("ERROR...")
logger.setLevel('ERROR')

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.error("-")

logger.error("WARNING...")
logger.setLevel('WARNING')

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.error("-")

logger.error("INFO...")
logger.setLevel('INFO')

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.error("-")


logger.error("DEBUG...")
logger.setLevel('DEBUG')

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.error("-")

