"""
Created on 15 Sep 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://pymotw.com/2/subprocess/
"""

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

    def o(self, args, wait=False):
        p = Popen(self.__cmd(args), stdout=PIPE)

        if wait:
            p.wait()

        return p


    def io(self, p, args, wait=False):
        p = Popen(self.__cmd(args), stdin=p.stdout, stdout=PIPE)

        if wait:
            p.wait()

        return p


    def i(self, p, args, wait=True):
        p = Popen(self.__cmd(args), stdin=p.stdout)

        if wait:
            p.wait()


    def __cmd(self, args):
        strs = [str(arg) for arg in args if arg is not None]

        return strs[:1] + ['-v'] + strs[1:] if self.__verbose else strs


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Command:{verbose:%s}" % self.verbose
