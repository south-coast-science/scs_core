"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.csv.csv_log_cursor import CSVLogCursor, CSVLogCursorQueue
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

    @classmethod
    def read(cls, cursor: CSVLogCursor):
        reader = CSVReader.construct_for_file(cursor.file_path, empty_string_as_null=True, start_row=cursor.row_number)

        try:
            cls.__read_rows(reader)
        finally:
            reader.close()


    @classmethod
    def tail(cls, cursor: CSVLogCursor):
        tail = Tail.construct(cursor.file_path)
        tail.open()

        reader = CSVReader(tail, empty_string_as_null=True, start_row=cursor.row_number)

        try:
            cls.__read_rows(reader)
        finally:
            reader.close()
            tail.close()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __read_rows(cls, reader):
        try:
            for datum in reader.rows():
                print(datum)
                sys.stdout.flush()

        except (BrokenPipeError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        cursor_queue = CSVLogCursorQueue(OrderedDict())
        cursor_queue.as_list(self._value)


    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        try:
            while True:
                with self._lock:
                    cursor_queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
                    cursor = cursor_queue.pop()

                    cursor_queue.as_list(self._value)

                if cursor is None:
                    time.sleep(self.__IDLE_TIME)
                    continue

                self.tail(cursor) if cursor.is_live else self.read(cursor)

        except (BrokenPipeError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # setters for client process...

    def initialise(self, cursor_queue: CSVLogCursorQueue):
        with self._lock:
            cursor_queue.as_list(self._value)


    def include(self, cursor: CSVLogCursor):
        with self._lock:
            cursor_queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
            cursor_queue.include(cursor)

            cursor_queue.as_list(self._value)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogReader:{cursor_queue:%s}" % CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
