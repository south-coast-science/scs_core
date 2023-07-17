"""
Created on 15 Sep 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://pymotw.com/2/subprocess/
"""

import sys

from subprocess import Popen, PIPE

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class Command(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose):
        """
        Constructor
        """
        self.__verbose = verbose                            # bool
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def s(self, cmd_args, wait=True, no_verbose=False):
        tokens = self.__cmd(cmd_args, no_verbose=no_verbose)
        self.__logger.info(' '.join(tokens))

        p = Popen(' '.join(tokens), shell=True)

        if wait:
            p.wait()


    def o(self, cmd_args, wait=False):
        tokens = self.__cmd(cmd_args)
        self.__logger.info(' '.join(tokens))

        p = Popen(tokens, stdout=PIPE)

        if wait:
            p.wait()

        return p


    def io(self, p, cmd_args, wait=False):
        tokens = self.__cmd(cmd_args)
        self.__logger.info(' '.join(tokens))

        p = Popen(tokens, stdin=p.stdout, stdout=PIPE)

        if wait:
            p.wait()

        return p


    def i(self, p, cmd_args, wait=True):
        tokens = self.__cmd(cmd_args)
        self.__logger.info(' '.join(tokens))

        p = Popen(tokens, stdin=p.stdout, stdout=sys.stderr)

        if wait:
            p.wait()


    # ----------------------------------------------------------------------------------------------------------------

    def __cmd(self, cmd_args, no_verbose=False):
        strs = [str(cmd_arg) for cmd_arg in cmd_args if cmd_arg is not None]

        if no_verbose:
            return strs

        return strs[:1] + ['-v'] + strs[1:] if self.__verbose else strs


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Command:{verbose:%s}" % self.verbose
