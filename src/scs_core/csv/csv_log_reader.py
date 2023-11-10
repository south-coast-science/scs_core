"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/51700960/runtimeerror-generator-raised-stopiteration-every-time-i-try-to-run-app
"""

import sys
import time

from collections import OrderedDict
from multiprocessing import Manager

from requests.exceptions import ConnectionError

from scs_core.aws.manager.byline.byline_finder import DeviceBylineFinder
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.csv.csv_log_cursor_queue import CSVLogCursorQueue, CSVLogCursor
from scs_core.csv.csv_reader import CSVReader

from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_core.sys.logging import Logging
from scs_core.sys.tail import Tail


# --------------------------------------------------------------------------------------------------------------------

class CSVLogReader(SynchronisedProcess):
    """
    classdocs
    """

    __IDLE_TIME =       4.0                 # seconds

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __read_rows(cls, reader):
        try:
            for datum in reader.rows():
                print(datum)
                sys.stdout.flush()

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, queue_builder, nullify=False):
        """
        Constructor
        """
        self.__logger = Logging.getLogger()
        self.__logging_specification = Logging.specification()

        manager = Manager()

        SynchronisedProcess.__init__(self, value=manager.list())

        queue = CSVLogCursorQueue()

        with self._lock:
            queue.as_list(self._value)

        self.__queue_builder = queue_builder                                    # CSVLogQueueBuilder
        self.__nullify = bool(nullify)                                          # bool


    # ----------------------------------------------------------------------------------------------------------------

    def run(self, halt_on_empty_queue=False):
        Logging.replicate(self.__logging_specification)
        self.__logger = Logging.getLogger()

        try:
            # build queue...
            timeline_start, cursors = self.__queue_builder.find_cursors()       # waits indefinitely for network

            self.__logger.info("timeline_start: %s" % timeline_start)

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

                self.__logger.info("reading: %s" % cursor)

                # process...
                read_count = self.__tail(cursor) if cursor.is_live else self.__read(cursor)

                self.__logger.info("closing: %s: read: %s" % (cursor, read_count))

                # remove...
                with self._lock:
                    queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
                    queue.remove(cursor.file_path)
                    queue.as_list(self._value)

                # self.__logger.info("*** removed cursor: %s" % cursor)

                if not cursor.is_live:
                    continue

                # try tailed file again...
                with self._lock:
                    tailed = CSVLogCursor(cursor.file_path, read_count, False)
                    queue = CSVLogCursorQueue.construct_from_jdict(OrderedDict(self._value))
                    queue.include(tailed)
                    queue.as_list(self._value)

                self.__logger.info("added tailed cursor: %s" % tailed)

        except FileNotFoundError as ex:
            self.__logger.error(repr(ex))

        except (ConnectionError, EOFError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # run methods...

    def __read(self, cursor: CSVLogCursor):
        reader = CSVReader.construct_for_file(cursor.file_path, nullify=self.__nullify, start_row=cursor.row)
        try:
            self.__read_rows(reader)

        finally:
            reader.close()

            return reader.read_count


    def __tail(self, cursor: CSVLogCursor):
        tail = Tail.construct(cursor.file_path)
        tail.open()

        reader = CSVReader(tail, nullify=self.__nullify, start_row=cursor.row)
        try:
            self.__read_rows(reader)

        except RuntimeError:            # Python 3.7 response to StopIteration
            pass                        # file is closed - but were all the rows read?!?

        except TimeoutError:
            self.__logger.error("TimeoutError: %s: read: %s" % (cursor, reader.read_count))

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

        return "CSVLogReader:{queue_builder:%s, queue:%s, nullify:%s}" % \
               (self.__queue_builder, queue, self.__nullify)


# --------------------------------------------------------------------------------------------------------------------

class CSVLogQueueBuilder(object):
    """
    classdocs
    """

    __BYLINE_WAIT_TIME = 20.0                   # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, conf, credentials, message_tag, topic_name, topic_path):
        """
        Constructor
        """
        self.__conf = conf                                      # CSVLoggerConf
        self.__credentials = credentials                        # CognitoDeviceCredentials
        self.__message_tag = message_tag                        # string
        self.__topic_name = topic_name                          # string
        self.__topic_path = topic_path                          # string

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def find_cursors(self):
        gatekeeper = CognitoLoginManager()
        finder = DeviceBylineFinder()

        # timeline_start...
        while True:
            try:
                auth = gatekeeper.device_login(self.__credentials)
                byline = finder.find_byline_for_topic(auth.id_token, self.__topic_path)
                break

            except ConnectionError as ex:
                self.__logger.info(ex)
                time.sleep(self.__BYLINE_WAIT_TIME)

        rec = None if byline is None else byline.rec
        byline_start = None if rec is None else rec.utc_datetime

        timeline_start = self.__conf.utc_retrospection_start(byline_start)

        # CSVLog...
        read_log = self.__conf.csv_log(self.__topic_name, tag=self.__message_tag, timeline_start=timeline_start)

        return timeline_start, CSVLogCursorQueue.find_cursors_for_log(read_log, 'rec')  # may raise FileNotFoundError


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self):
        return "CSVLogQueueBuilder:{conf:%s, credentials:%s, message_tag:%s, topic_name:%s, topic_path:%s}" % \
               (self.__conf, self.__credentials, self.__message_tag, self.__topic_name, self.__topic_path)
