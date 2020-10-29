"""
Created on 28 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

import time
from collections import OrderedDict
from multiprocessing import Manager

from scs_core.aws.monitor.email_queue import EmailQueue
from scs_core.sync.synchronised_process import SynchronisedProcess


class EmailQueueManager(SynchronisedProcess):
    __WAIT_PERIOD = 1 # seconds
    def __init__(self):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())


    def run(self):
        while True:
            k, v = None, None

            try:
                with self._lock:
                    if not self._value is None:
                        queue = EmailQueue.construct_from_jdict(OrderedDict(self._value))
                        k, v = queue.pop_next()
                        # self.set_queue(queue)
                print(k, v)
                time.sleep(self.__WAIT_PERIOD)
            except (ConnectionError, KeyboardInterrupt, SystemExit):
                pass

    def set_queue(self, queue):
        with self._lock:
            queue.as_list(self._value)
            # print(self._value)

