"""
Created on 28 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.data.average import Average

from scs_core.gas.ndir_datum import NDIRDatum

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_host.lock.lock_timeout import LockTimeout


# --------------------------------------------------------------------------------------------------------------------

class NDIRMonitor(SynchronisedProcess):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ndir, conf):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__ndir = ndir
        self.__averaging = Average(conf.tally)


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def start(self):
        try:
            self.__ndir.power_on()
            self.__averaging.reset()

            super().start()

        except KeyboardInterrupt:
            pass


    def stop(self):
        try:
            super().stop()

            self.__ndir.power_off()

        except KeyboardInterrupt:
            pass

        except LockTimeout:
            pass


    def run(self):
        try:
            timer = IntervalTimer(self.__ndir.sample_interval())

            while timer.true():
                sample = self.__ndir.sample()

                self.__averaging.append(sample)
                average = self.__averaging.compute()

                # report...
                with self._lock:
                    average.as_list(self._value)

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # data retrieval for client process...

    def firmware(self):
        return self.__ndir.version()


    def sample(self):
        with self._lock:
            value = self._value

        return NDIRDatum.construct_from_jdict(OrderedDict(value))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRMonitor:{value:%s, averaging:%s, ndir:%s}" % \
               (self._value, self.__averaging, self.__ndir)
