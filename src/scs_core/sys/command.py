"""
Created on 15 Sep 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://pymotw.com/2/subprocess/
"""
import sys
from subprocess import Popen, PIPE


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
        self.__verbose = verbose                    # bool


    # ----------------------------------------------------------------------------------------------------------------

    def o(self, cmd_args, wait=False):
        p = Popen(self.__cmd(cmd_args), stdout=PIPE)

        if wait:
            p.wait()

        return p


    def io(self, p, cmd_args, wait=False):
        p = Popen(self.__cmd(cmd_args), stdin=p.stdout, stdout=PIPE)

        if wait:
            p.wait()

        return p


    def i(self, p, cmd_args, wait=True):
        p = Popen(self.__cmd(cmd_args), stdin=p.stdout, stdout=sys.stderr)

        if wait:
            p.wait()


    def __cmd(self, cmd_args):
        strs = [str(cmd_arg) for cmd_arg in cmd_args if cmd_arg is not None]

        return strs[:1] + ['-v'] + strs[1:] if self.__verbose else strs


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Command:{verbose:%s}" % self.verbose
