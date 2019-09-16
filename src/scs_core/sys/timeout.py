"""
Created on 16 Sep 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Usage:

timeout = Timeout(10)

try:
    with timeout:
        my_func()

except TimeoutError:
    print("my_func() timed out!")

https://www.jujens.eu/posts/en/2018/Jun/02/python-timeout-function/
"""

import signal


# --------------------------------------------------------------------------------------------------------------------

class Timeout(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def raise_timeout(_signum, _frame):
        signal.signal(signal.SIGALRM, signal.SIG_IGN)

        raise TimeoutError


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, seconds):
        """
        Constructor
        """
        self.__seconds = seconds                                    # number


    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(int(round(self.__seconds)))


    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Timeout:{seconds:%s}" % self.__seconds
