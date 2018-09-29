"""
Created on 27 Sep 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://eli.thegreenplace.net/2012/01/04/shared-counter-with-pythons-multiprocessing/
"""

import time

from multiprocessing import Manager

from scs_core.sync.synchronised_process import SynchronisedProcess


# --------------------------------------------------------------------------------------------------------------------

# noinspection PyBroadException

class MessageQueue(SynchronisedProcess):
    """
    classdocs
    """

    LOCK_RELEASE_TIME =     0.2

    __DO_ENQ =          'do_enq'
    __DO_DEQ =          'do_deq'
    __LENGTH =          'len'
    __NEWEST =          'new'
    __OLDEST =          'old'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, max_size):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.dict())

        self.__max_size = max_size

        self.__messages = []

        self._value[self.__DO_ENQ] = False
        self._value[self.__DO_DEQ] = False
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
                time.sleep(self.LOCK_RELEASE_TIME)

                with self._lock:
                    if not (self._value[self.__DO_ENQ] or self._value[self.__DO_DEQ]):
                        continue

                    if self._value[self.__DO_ENQ]:
                        self.__set_newest(self._value[self.__NEWEST])
                        self._value[self.__DO_ENQ] = False

                    if self._value[self.__DO_DEQ]:
                        self.__pop_oldest()
                        self._value[self.__DO_DEQ] = False

                    self._value[self.__OLDEST] = self.__get_oldest()
                    self._value[self.__LENGTH] = len(self)

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # client accessors...

    def enqueue(self, message):
        try:
            with self._lock:
                self._value[self.__DO_ENQ] = True
                self._value[self.__NEWEST] = message

            time.sleep(self.LOCK_RELEASE_TIME)              # wait for run loop to regain lock

        except BaseException:
            pass


    def dequeue(self):
        try:
            with self._lock:
                self._value[self.__DO_DEQ] = True

            time.sleep(self.LOCK_RELEASE_TIME)              # wait for run loop to regain lock

        except BaseException:
            pass


    def next(self):
        try:
            with self._lock:
                return self._value[self.__OLDEST]

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
            return

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
        return "MessageQueue:{max_size:%s, value:{do_enq:%s, do_deq:%s, len:%s, old:%s, new:%s}}" % \
               (self.__max_size, self._value[self.__DO_ENQ], self._value[self.__DO_DEQ], self._value[self.__LENGTH],
                self._value[self.__OLDEST], self._value[self.__NEWEST])
