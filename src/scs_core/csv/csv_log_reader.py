"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/51700960/runtimeerror-generator-raised-stopiteration-every-time-i-try-to-run-app
"""

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

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, queue_builder, empty_string_as_null=False, reporter=None):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        queue = CSVLogCursorQueue()

        with self._lock:
            queue.as_list(self._value)

        self.__queue_builder = queue_builder                                    # CSVLogQueueBuilder
        self.__empty_string_as_null = bool(empty_string_as_null)                # bool
        self.__reporter = reporter                                              # CSVLogReporter


    # ----------------------------------------------------------------------------------------------------------------

    def run(self, halt_on_empty_queue=False):
        try:
            # build queue...
            timeline_start, cursors = self.__queue_builder.find_cursors()       # waits indefinitely for network

            if self.__reporter:
                self.__reporter.timeline_start(timeline_start)

            with self._lock:
                queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
                for cursor in cursors:
                    queue.include(cursor)
                queue.as_list(self._value)

            # drain queue...
            while True:
                # find oldest...
                with self._lock:
                    queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
                    cursor = queue.next()
                    queue.as_list(self._value)

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

        except (ConnectionError, EOFError, KeyboardInterrupt, SystemExit):
            pass

        except FileNotFoundError as ex:                     # parent process is terminating
            self.__reporter.exception(ex)


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

        cursor = CSVLogCursor(file_path, 0, True)

        with self._lock:
            queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
            queue.include(cursor)
            queue.as_list(self._value)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        with self._lock:
            queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))

        return "CSVLogReader:{queue_builder:%s, queue:%s, empty_string_as_null:%s, reporter:%s}" % \
               (self.__queue_builder, queue, self.__empty_string_as_null, self.__reporter)


# --------------------------------------------------------------------------------------------------------------------

class CSVLogQueueBuilder(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic_name, topic_path, byline_manager, system_id, conf):
        self.__topic_name = topic_name
        self.__topic_path = topic_path
        self.__byline_manager = byline_manager
        self.__system_id = system_id
        self.__conf = conf


    # ----------------------------------------------------------------------------------------------------------------

    def find_cursors(self):                                                     # waits indefinitely for network
        # timeline_start...
        byline = self.__byline_manager.find_byline_for_device_topic(self.__system_id.message_tag(), self.__topic_path)
        timeline_start = None if byline is None else byline.rec.datetime

        # CSVLog...
        read_log = self.__conf.csv_log(self.__topic_name, tag=self.__system_id.message_tag(),
                                       timeline_start=timeline_start)

        return timeline_start, CSVLogCursorQueue.find_cursors_for_log(read_log, 'rec')


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self):
        return "CSVLogQueueBuilder:{topic_name:%s, topic_path:%s, byline_manager:%s, system_id:%s, conf:%s}" % \
               (self.__topic_name, self.__topic_path, self.__byline_manager, self.__system_id, self.__conf)


# --------------------------------------------------------------------------------------------------------------------

class CSVLogReporter(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def opening(self, cursor):
        pass


    @abstractmethod
    def timeline_start(self, timeline_start):
        pass


    @abstractmethod
    def closing(self, cursor, read_count):
        pass


    @abstractmethod
    def timeout(self, cursor, read_count):
        pass


    @abstractmethod
    def exception(self, ex):
        pass
