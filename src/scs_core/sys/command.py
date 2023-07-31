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

    def s(self, cmd_args, wait=True, no_verbose=False, abort_on_fail=True):
        tokens = self.__cmd(cmd_args, no_verbose=no_verbose)
        p = Popen(' '.join(tokens), shell=True)

        return self.__process(p, wait=wait, abort_on_fail=abort_on_fail)


    def o(self, cmd_args, wait=False, abort_on_fail=True):
        tokens = self.__cmd(cmd_args)
        p = Popen(tokens, stdout=PIPE)

        return self.__process(p, wait=wait, abort_on_fail=abort_on_fail)


    def io(self, p, cmd_args, wait=False, abort_on_fail=True):
        tokens = self.__cmd(cmd_args)
        p = Popen(tokens, stdin=p.stdout, stdout=PIPE)

        return self.__process(p, wait=wait, abort_on_fail=abort_on_fail)


    def i(self, p, cmd_args, wait=True, abort_on_fail=True):
        tokens = self.__cmd(cmd_args)
        p = Popen(tokens, stdin=p.stdout, stdout=sys.stderr)

        return self.__process(p, wait=wait, abort_on_fail=abort_on_fail)


    # ----------------------------------------------------------------------------------------------------------------

    def __cmd(self, cmd_args, no_verbose=False):
        tokens = [str(cmd_arg) for cmd_arg in cmd_args if cmd_arg is not None]

        if self.__verbose and not no_verbose:
            tokens = tokens[:1] + ['-v'] + tokens[1:]

        self.__logger.info(' '.join(tokens))

        return tokens


    def __process(self, p, wait=False, abort_on_fail=True):
        if wait:
            p.wait()

        if abort_on_fail and (p.returncode is not None and p.returncode != 0):
            self.__logger.error('ABORTED.')
            exit(p.returncode)

        return p


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Command:{verbose:%s}" % self.verbose
