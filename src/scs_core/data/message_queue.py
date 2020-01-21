"""
Created on 27 Sep 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A shared queue supporting a single producer process and a single consumer process.
"""

import copy
import time

from multiprocessing import Manager

from scs_core.sync.synchronised_process import SynchronisedProcess


# --------------------------------------------------------------------------------------------------------------------

# noinspection PyBroadException

class MessageQueue(SynchronisedProcess):
    """
    classdocs
    """

    __PROCESS_LOCK_RELEASE_TIME =       0.1             # seconds
    __CLIENT_LOCK_RELEASE_TIME =        0.2             # seconds - must be longer than __PROCESS_LOCK_RELEASE_TIME


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, max_size):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, MessageQueueInterface(manager.dict()))

        self.__max_size = max_size                      # int
        self.__messages = []                            # array of JSONable messages


    def __len__(self):
        return len(self.__messages)


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def run(self):
        try:
            while True:
                time.sleep(self.__PROCESS_LOCK_RELEASE_TIME)            # wait for client operations

                with self._lock:
                    if not self._value.has_cmd():
                        continue

                    if self._value.cmd_enq:
                        self.__set_newest(self._value.newest)

                    if self._value.cmd_deq:
                        self.__pop_oldest()

                    self._value.clear_cmds()
                    self._value.oldest = self.__get_oldest()
                    self._value.length = len(self)

        except (BrokenPipeError, KeyboardInterrupt, SystemExit):
            return


    # ----------------------------------------------------------------------------------------------------------------
    # producer interface...

    def enqueue(self, message):
        try:
            with self._lock:
                self._value.cmd_enq = True
                self._value.newest = copy.deepcopy(message)

            time.sleep(self.__CLIENT_LOCK_RELEASE_TIME)                 # wait for queue to be processed

        except BaseException:
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # consumer interface...

    def dequeue(self):
        try:
            with self._lock:
                self._value.cmd_deq = True

            time.sleep(self.__CLIENT_LOCK_RELEASE_TIME)                 # wait for queue to be processed

        except BaseException:
            pass


    def length(self):
        try:
            with self._lock:
                length = self._value.length

            return length

        except BaseException:
            pass


    def next(self):
        try:
            with self._lock:
                oldest = copy.deepcopy(self._value.oldest)

            return oldest

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
        return "MessageQueue:{max_size:%s, interface:%s}" %  (self.__max_size, self._value)


# --------------------------------------------------------------------------------------------------------------------

class MessageQueueInterface(object):
    """
    classdocs
    """

    # fields...
    __ENQ =         'enq'
    __DEQ =         'deq'
    __LENGTH =      'len'
    __NEWEST =      'new'
    __OLDEST =      'old'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, value):
        """
        Constructor
        """
        self.__value = value                    # dict

        self.cmd_enq = False                    # bool
        self.cmd_deq = False                    # bool

        self.newest = None                      # JSONable message
        self.oldest = None                      # JSONable message
        self.length = 0                         # int


    # ----------------------------------------------------------------------------------------------------------------

    def has_cmd(self):
        return self.cmd_enq or self.cmd_deq


    def clear_cmds(self):
        self.cmd_enq = False
        self.cmd_deq = False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cmd_enq(self):
        return self.__value[self.__ENQ]


    @cmd_enq.setter
    def cmd_enq(self, enq):
        self.__value[self.__ENQ] = enq


    @property
    def cmd_deq(self):
        return self.__value[self.__DEQ]


    @cmd_deq.setter
    def cmd_deq(self, deq):
        self.__value[self.__DEQ] = deq


    @property
    def length(self):
        return self.__value[self.__LENGTH]


    @length.setter
    def length(self, length):
        self.__value[self.__LENGTH] = length


    @property
    def oldest(self):
        return self.__value[self.__OLDEST]


    @oldest.setter
    def oldest(self, oldest):
        self.__value[self.__OLDEST] = oldest


    @property
    def newest(self):
        return self.__value[self.__NEWEST]


    @newest.setter
    def newest(self, newest):
        self.__value[self.__NEWEST] = newest


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageQueueInterface:{cmd_enq:%s, cmd_deq:%s, length:%s, oldest:%s, newest:%s}}" % \
               (self.cmd_enq, self.cmd_deq, self.length, self.oldest, self.newest)
