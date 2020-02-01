"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/51700960/runtimeerror-generator-raised-stopiteration-every-time-i-try-to-run-app
"""

import copy
import sys
import time

from abc import ABC, abstractmethod
from collections import OrderedDict
from multiprocessing import Manager

from scs_core.csv.csv_log_cursor_queue import CSVLogCursorQueue, CSVLogCursor
from scs_core.csv.csv_reader import CSVReader

from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_core.sys.tail import Tail


# --------------------------------------------------------------------------------------------------------------------

class CSVLogReader(SynchronisedProcess):
    """
    classdocs
    """

    __IDLE_TIME =       4.0                 # seconds

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __read_rows(reader):
        try:
            for datum in reader.rows():
                print(datum)
                sys.stdout.flush()

        except (BrokenPipeError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, queue: CSVLogCursorQueue, empty_string_as_null=False, reporter=None):
        """
        Constructor
        """
        # print("*** CSVLogReader: queue: %s" % queue, file=sys.stderr)
        # sys.stderr.flush()

        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        with self._lock:
            queue.as_list(self._value)

        # print("*** CSVLogReader: self._value: %s" % self._value, file=sys.stderr)
        # sys.stderr.flush()

        self.__empty_string_as_null = bool(empty_string_as_null)                # bool
        self.__reporter = reporter                                              # CSVLogReaderReporter


    # ----------------------------------------------------------------------------------------------------------------

    def run(self, halt_on_empty_queue=False):
        try:
            while True:
                # find oldest...
                with self._lock:
                    try:
                        # print("*** CSVLogReader.run: self._value: %s" % self._value, file=sys.stderr)
                        # sys.stderr.flush()

                        queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
                        cursor = queue.next()
                        queue.as_list(self._value)

                    except FileNotFoundError as ex:
                        print("*** CSVLogReader.run: %s" % ex, file=sys.stderr)
                        sys.stderr.flush()

                        cursor = None

                if cursor is None:
                    if halt_on_empty_queue:
                        return
                    else:
                        time.sleep(self.__IDLE_TIME)
                        continue

                if self.__reporter:
                    self.__reporter.opening(cursor)

                # process...
                read_count = self.__tail(cursor) if cursor.is_live else self.__read(cursor)

                if self.__reporter:
                    self.__reporter.closing(cursor, read_count)

                # remove...
                with self._lock:
                    queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
                    queue.remove(cursor.file_path)
                    queue.as_list(self._value)

        except (BrokenPipeError, ConnectionResetError, EOFError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # run methods...

    def __read(self, cursor: CSVLogCursor):
        reader = CSVReader.construct_for_file(cursor.file_path,
                                              empty_string_as_null=self.__empty_string_as_null, start_row=cursor.row)
        try:
            self.__read_rows(reader)

        finally:
            reader.close()

            return reader.read_count


    def __tail(self, cursor: CSVLogCursor):
        tail = Tail.construct(cursor.file_path)
        tail.open()

        reader = CSVReader(tail,
                           empty_string_as_null=self.__empty_string_as_null, start_row=cursor.row)
        try:
            self.__read_rows(reader)

        except RuntimeError:
            pass                                # Python 3.7 response to StopIteration

        except TimeoutError:
            if self.__reporter:
                self.__reporter.timeout(cursor, reader.read_count)

        finally:
            reader.close()
            tail.close()

            return reader.read_count


    # ----------------------------------------------------------------------------------------------------------------
    # setters for client process...

    def include(self, file_path):
        if file_path is None:
            return

        with self._lock:
            queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
            queue.include(file_path, True)
            queue.as_list(self._value)



    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        with self._lock:
            queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))

        return "CSVLogReader:{queue:%s, empty_string_as_null:%s, reporter:%s}" % \
               (queue, self.__empty_string_as_null, self.__reporter)


# --------------------------------------------------------------------------------------------------------------------

class CSVLogReaderReporter(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def opening(self, cursor):
        pass


    @abstractmethod
    def closing(self, cursor, read_count):
        pass


    @abstractmethod
    def timeout(self, cursor, read_count):
        pass
