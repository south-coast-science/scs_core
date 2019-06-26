"""
Created on 26 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import signal
import sys


# --------------------------------------------------------------------------------------------------------------------

# noinspection PyUnusedLocal

class SignalledExit(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls, client, verbose):
        listener = cls(client, verbose)

        listener.__original_sigint_handler = signal.getsignal(signal.SIGINT)        # function

        signal.signal(signal.SIGINT, listener.sigint_handler)
        signal.signal(signal.SIGTERM, listener.sigterm_handler)

        return listener


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client, verbose):
        """
        Constructor
        """
        self.__client = client                                  # string
        self.__verbose = verbose                                # bool

        self.__exiting = False                                  # bool
        self.__original_sigint_handler = None                   # function


    # ----------------------------------------------------------------------------------------------------------------

    def clear(self):
        if self.__original_sigint_handler is None:
            return

        signal.signal(signal.SIGINT, self.__original_sigint_handler)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)


    # ----------------------------------------------------------------------------------------------------------------

    def sigint_handler(self, signum, frame):
        if self.__exiting:
            return

        self.clear()
        self.__exiting = True

        if self.__verbose:
            print("%s: SIGINT" % self.__client, file=sys.stderr)

        sys.exit(1)


    def sigterm_handler(self, signum, frame):
        if self.__exiting:
            return

        self.clear()
        self.__exiting = True

        if self.__verbose:
            print("%s: SIGTERM" % self.__client, file=sys.stderr)

        sys.exit(0)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SignalledExit:{client:%s, verbose:%s, exiting:%s, original_sigint_handler:%s}" % \
               (self.__client, self.__verbose, self.__exiting, self.__original_sigint_handler)
