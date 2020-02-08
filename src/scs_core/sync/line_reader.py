"""
Created on 14 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A portable, non-blocking Python line reader. Yes, such a thing exists. And this is it...
"""

import os

from multiprocessing import Process, Queue


# --------------------------------------------------------------------------------------------------------------------

class LineReader(object):
    """
    classdocs
    """
    def __init__(self, fileno):
        """
        Constructor
        """
        self.__fileno = fileno
        self.__queue = Queue()


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        proc = Process(target=self.run)
        proc.start()

        return proc


    def run(self):
        file = os.fdopen(self.__fileno)

        try:
            for line in file:
                self.__queue.put(str(line).strip())

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass

        self.__queue.put(None)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def lines(self):
        while True:
            if self.__queue.empty():
                line = None

            else:
                line = self.__queue.get()

                if line is None:
                    return

            yield line


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LineReader:{fileno:%s, queue:%s}" % (self.__fileno, self.__queue)
