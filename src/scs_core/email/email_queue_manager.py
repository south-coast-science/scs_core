"""
Created on 28 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

import time

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.email.email_queue import EmailQueue

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class EmailQueueManager(SynchronisedProcess):

    __WAIT_PERIOD = 10  # seconds
    __MAX_NUM_RETRIES = 5


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, email_client):
        """
        Constructor
        """
        self.__logger = Logging.getLogger()
        self.__logging_specification = Logging.specification()

        manager = Manager()

        SynchronisedProcess.__init__(self, value=manager.list())

        self.__email_client = email_client


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        self.__email_client.open_server()
        super().start()


    def stop(self):
        time.sleep(self.__WAIT_PERIOD * 2)
        super().stop()


    def run(self):
        Logging.replicate(self.__logging_specification)

        try:
            timer = IntervalTimer(10)

            while timer.true():
                k, v = None, None
                if self._value is not None:
                    with self._lock:
                        queue = EmailQueue.construct_from_jdict(OrderedDict(self._value))
                        if queue is not None:
                            k, v = queue.pop_next()
                    if k is not None and v is not None:
                        if self.__email_client.send_mime_email(v, k):
                            self.set_queue(queue)

                time.sleep(self.__WAIT_PERIOD)

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    def set_queue(self, queue):
        with self._lock:
            queue.as_list(self._value)

        return True


    def get_queue(self):
        with self._lock:
            queue = EmailQueue.construct_from_jdict(OrderedDict(self._value))

        return queue


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "EmailQueueManager:{queue:%s}" % self.get_queue()
