"""
Created on 26 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import signal
import sys

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class SignalledExit(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls):
        listener = cls()
        listener.set()

        return listener


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__original_sigint_handler = None                   # function?
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def sigint_handler(self, signum, _frame):
        self.clear()

        self.__logger.info("SIGINT (%d)" % signum)

        sys.exit(1)


    def sigterm_handler(self, signum, _frame):
        self.clear()

        self.__logger.info("SIGTERM (%d)" % signum)

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
        return "SignalledExit:{original_sigint_handler:%s}" % self.__original_sigint_handler
