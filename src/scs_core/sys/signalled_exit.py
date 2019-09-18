"""
Created on 26 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import signal
import sys


# --------------------------------------------------------------------------------------------------------------------

class SignalledExit(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, client, verbose):
        listener = cls(client, verbose)
        listener.set()

        return listener


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client, verbose):
        """
        Constructor
        """
        self.__client = client                                  # string
        self.__verbose = verbose                                # bool

        self.__original_sigint_handler = None                   # function?


    # ----------------------------------------------------------------------------------------------------------------

    def sigint_handler(self, signum, _frame):
        self.clear()

        if self.__verbose:
            print("%s: SIGINT (%d)" % (self.__client, signum), file=sys.stderr)
            sys.stderr.flush()

        sys.exit(1)


    def sigterm_handler(self, signum, _frame):
        self.clear()

        if self.__verbose:
            print("%s: SIGTERM (%d)" % (self.__client, signum), file=sys.stderr)
            sys.stderr.flush()

        sys.exit(0)


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        if self.__original_sigint_handler is None:
            self.__original_sigint_handler = signal.getsignal(signal.SIGINT)

        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigterm_handler)


    def clear(self):
        if self.__original_sigint_handler is None:
            return

        signal.signal(signal.SIGINT, self.__original_sigint_handler)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SignalledExit:{client:%s, verbose:%s, original_sigint_handler:%s}" % \
               (self.__client, self.__verbose, self.__original_sigint_handler)
