"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

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

    __IDLE_TIME =       2.0                 # seconds

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

    def __init__(self, queue: CSVLogCursorQueue, empty_string_as_null=False, verbose=False):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        with self._lock:
            queue.as_list(self._value)

        self.__empty_string_as_null = bool(empty_string_as_null)                # bool
        self.__verbose = bool(verbose)                                          # bool


    # ----------------------------------------------------------------------------------------------------------------

    def run(self, halt_on_empty_queue=False):
        try:
            while True:
                with self._lock:
                    queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
                    cursor = queue.pop()

                    queue.as_list(self._value)

                if cursor is None:
                    if halt_on_empty_queue:
                        return
                    else:
                        time.sleep(self.__IDLE_TIME)
                        continue

                if self.__verbose:
                    print("CSVLogReader: %s" % cursor, file=sys.stderr)
                    sys.stderr.flush()

                self.__tail(cursor) if cursor.is_live else self.__read(cursor)

        except (BrokenPipeError, ConnectionResetError, EOFError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # run methods...

    def __read(self, cursor: CSVLogCursor):
        reader = CSVReader.construct_for_file(cursor.file_path,
                                              empty_string_as_null=self.__empty_string_as_null,
                                              start_row=cursor.row_number)
        try:
            self.__read_rows(reader)
        finally:
            reader.close()


    def __tail(self, cursor: CSVLogCursor):
        tail = Tail.construct(cursor.file_path)
        tail.open()

        reader = CSVReader(tail,
                           empty_string_as_null=self.__empty_string_as_null,
                           start_row=cursor.row_number)
        try:
            self.__read_rows(reader)

        except RuntimeError:
            pass                    # catches StopIteration

        except TimeoutError:
            print("CSVLogReader: %s: TimeoutError" % cursor.file_path, file=sys.stderr)
            sys.stderr.flush()

        finally:
            reader.close()
            tail.close()


    # ----------------------------------------------------------------------------------------------------------------
    # setters for client process...

    def set_live(self, file_path):
        with self._lock:
            queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
            queue.set_live(file_path)

            queue.as_list(self._value)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        with self._lock:
            queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))

        return "CSVLogReader:{queue:%s, empty_string_as_null:%s, verbose:%s}" % \
               (queue, self.__empty_string_as_null, self.__verbose)
