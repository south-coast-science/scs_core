"""
Created on 27 Sep 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://eli.thegreenplace.net/2012/01/04/shared-counter-with-pythons-multiprocessing/
"""

import sys
import time

from multiprocessing import Manager

from scs_core.sync.synchronised_process import SynchronisedProcess


# --------------------------------------------------------------------------------------------------------------------

# noinspection PyBroadException

class MessageQueue(SynchronisedProcess):
    """
    classdocs
    """

    __CMD_ENQUEUE =     'enq'
    __CMD_REMOVE =      'rem'

    __CMD =             'cmd'
    __NEWEST =          'new'
    __OLDEST =          'old'
    __LENGTH =          'len'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, max_size):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.dict())

        self.__max_size = max_size

        self.__messages = []

        self._value[self.__CMD] = None
        self._value[self.__NEWEST] = None
        self._value[self.__OLDEST] = None
        self._value[self.__LENGTH] = 0


    def __len__(self):
        return len(self.__messages)


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def run(self):
        try:
            while True:
                time.sleep(0.1)

                with self._lock:
                    cmd = self._value[self.__CMD]

                    if not cmd:
                        time.sleep(0.1)                     # don't thrash the CPU
                        continue

                    self._value[self.__CMD] = None

                    if cmd == self.__CMD_ENQUEUE:
                        self.__set_newest(self._value[self.__NEWEST])

                    elif cmd == self.__CMD_REMOVE:
                        self.__pop_oldest()

                    self._value[self.__OLDEST] = self.__get_oldest()
                    self._value[self.__LENGTH] = len(self)

                    print("cmd done: %s" % cmd, file=sys.stderr)
                    sys.stderr.flush()

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # client accessors...

    def enqueue(self, message):
        try:
            with self._lock:
                self._value[self.__NEWEST] = message
                self._value[self.__CMD] = self.__CMD_ENQUEUE

            time.sleep(0.2)

        except BaseException:
            pass


    def oldest(self):
        try:
            with self._lock:
                return self._value[self.__OLDEST]

        except BaseException:
            pass


    def remove_oldest(self):
        try:
            with self._lock:
                self._value[self.__CMD] = self.__CMD_REMOVE

            time.sleep(0.2)

        except BaseException:
            pass


    def length(self):
        try:
            with self._lock:
                return self._value[self.__LENGTH]

        except BaseException:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def __set_newest(self, message):
        if self.__is_full():
            self.__messages.pop(0)

        self.__messages.append(message)


    def __get_oldest(self):
        if self.__is_empty():
            return None

        return self.__messages[0]


    def __pop_oldest(self):
        if self.__is_empty():
            return

        self.__messages.pop(0)


    def __is_empty(self):
        return len(self) == 0


    def __is_full(self):
        return len(self) >= self.__max_size


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageQueue:{max_size:%s, value:%s}" % (self.__max_size, self._value)
