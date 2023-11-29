#!/usr/bin/env python3

"""
Created on 20 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sys.command import Command
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

Logging.config('command_test')

command = Command(verbose=True)

command.s(['rm', 'non-existent.txt'], no_verbose=True, abort_on_fail=False)
command.s(['ls'], no_verbose=True)
