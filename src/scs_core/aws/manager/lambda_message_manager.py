"""
Created on 26 Nov 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

This version of MessageManager for AWS lambda function with multipart response.

Equivalent to cURL:
curl "https://aws.southcoastscience.com/topicMessages?topic=unep/ethiopia/loc/1/climate
&startTime=2018-12-13T07:03:59.712Z&endTime=2018-12-13T15:10:59.712Z"

Test endpoint:
curl "https://hb7aqje541.execute-api.us-west-2.amazonaws.com/default/AWSAggregateTest?topic=unep/ethiopia/loc/1/climate
&startTime=2018-12-13T07:03:59.712Z&endTime=2018-12-13T15:10:59.712Z"
"""

from collections import OrderedDict
from urllib.parse import urlparse, parse_qs

from scs_core.aws.client.api_intercourse import APIResponse
from scs_core.aws.client.rest_client import RESTClient

from scs_core.aws.data.message import Message

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.str import Str
from scs_core.data.timedelta import Timedelta

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class MessageManager(object):
    """
    classdocs AWSAggregateTest
    """

    __REQUEST_PATH = '/topicMessages'

    # __REQUEST_PATH = '/default/AWSAggregateTest'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reporter=None, api_key=None):
        """
        Constructor
        """
        self.__rest_client = RESTClient(api_key=api_key)
        self.__reporter = reporter
        self.__api_key = api_key

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def find_latest_for_topic(self, topic, end, path, include_wrapper, rec_only, backoff_limit):
        documents = list(self.find_for_topic(topic, None, end, path, False, None, include_wrapper, rec_only, False,
                                             False, True, backoff_limit))
        if documents:
            return documents[0]

        return None


    def find_for_topic(self, topic, start, end, path, fetch_last, checkpoint, include_wrapper, rec_only,
                       min_max, exclude_remainder, fetch_last_written_before, backoff_limit):
        self.__reporter.reset()

        request = MessageRequest(topic, start, end, path, fetch_last, checkpoint, include_wrapper, rec_only,
                                 min_max, exclude_remainder, fetch_last_written_before, backoff_limit)
        self.__logger.debug(request)

        params = request.params()

        # request...
        self.__rest_client.connect()

        try:
            while True:
                jdict = self.__rest_client.get(self.__REQUEST_PATH, params)

                # messages...
                block = MessageResponse.construct_from_jdict(jdict)
                self.__logger.debug(block)

                for item in block.items:
                    yield item

                # report...
                if self.__reporter:
                    self.__reporter.print(len(block), block_start=block.start())

                # next request...
                if block.next_url is None:
                    break

                next_url = urlparse(block.next_url)
                next_params = parse_qs(next_url.query)

                # noinspection PyTypeChecker
                params[MessageRequest.START] = next_params[MessageRequest.START][0]

        finally:
            self.__rest_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageManager:{rest_client:%s, reporter:%s, api_key:%s}" % \
            (self.__rest_client, self.__reporter, self.__api_key)


# --------------------------------------------------------------------------------------------------------------------

class MessageRequest(object):
    """
    classdocs
    """

    TOPIC = 'topic'
    START = 'startTime'
    END = 'endTime'
    PATH = 'path'
    FETCH_LAST_WRITTEN = 'fetchLastWritten'
    CHECKPOINT = 'checkpoint'
    INCLUDE_WRAPPER = 'includeWrapper'
    REC_ONLY = 'recOnly'
    MIN_MAX = 'minMax'
    EXCLUDE_REMAINDER = 'excludeRemainder'
    FETCH_LAST_WRITTEN_BEFORE = 'fetchLastWrittenBefore'
    BACKOFF_LIMIT = "backoffLimit"

    # ----------------------------------------------------------------------------------------------------------------

    __DAY = Timedelta(days=1)
    __WEEK = Timedelta(weeks=1)
    __MONTH = Timedelta(days=28)
    __YEAR = Timedelta(days=365)

    @classmethod
    def checkpoint_table(cls, start, end):
        delta = end - start

        if delta < cls.__DAY:
            return None  # raw data rate

        if delta < cls.__WEEK:
            return '**:/01:00'

        if delta < cls.__MONTH:
            return '**:/15:00'

        if delta < cls.__YEAR:
            return '**:00:00'

        return '/06:00:00'


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        # compulsory...
        topic = qsp.get(cls.TOPIC)
        start = LocalizedDatetime.construct_from_iso8601(qsp.get(cls.START))
        end = LocalizedDatetime.construct_from_iso8601(qsp.get(cls.END))

        # optional...
        path = qsp.get(cls.PATH)
        fetch_last_written = Datum.is_true(qsp.get(cls.FETCH_LAST_WRITTEN))
        checkpoint = qsp.get(cls.CHECKPOINT)
        include_wrapper = Datum.is_true(qsp.get(cls.INCLUDE_WRAPPER))
        rec_only = Datum.is_true(qsp.get(cls.REC_ONLY))
        min_max = Datum.is_true(qsp.get(cls.MIN_MAX))
        exclude_remainder = Datum.is_true(qsp.get(cls.EXCLUDE_REMAINDER))
        fetch_last_written_before = Datum.is_true(qsp.get(cls.FETCH_LAST_WRITTEN_BEFORE))
        backoff_limit = qsp.get(cls.backoff_limit)

        if checkpoint and checkpoint.lower() == 'none':
            checkpoint = None

        return cls(topic, start, end, path, fetch_last_written, checkpoint, include_wrapper, rec_only,
                   min_max, exclude_remainder, fetch_last_written_before, backoff_limit)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, start, end, path, fetch_last_written, checkpoint, include_wrapper, rec_only,
                 min_max, exclude_remainder, fetch_last_written_before, backoff_limit):
        """
        Constructor
        """
        self.__topic = topic                                                        # string
        self.__start = start                                                        # LocalizedDatetime
        self.__end = end                                                            # LocalizedDatetime

        self.__path = path                                                          # string
        self.__fetch_last_written = bool(fetch_last_written)                        # bool
        self.__checkpoint = checkpoint                                              # string
        self.__include_wrapper = bool(include_wrapper)                              # bool
        self.__rec_only = bool(rec_only)                                            # bool
        self.__min_max = bool(min_max)                                              # bool
        self.__exclude_remainder = bool(exclude_remainder)                          # bool
        self.__fetch_last_written_before = bool(fetch_last_written_before)          # bool
        self.__backoff_limit = backoff_limit                                        # int seconds


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.topic is None or self.start is None or self.end is None:
            return False

        now = LocalizedDatetime.now()

        if self.start > now or self.end > now:
            return False

        if self.start > self.end:
            return False

        if self.include_wrapper and self.checkpoint is not None:
            return False

        if self.rec_only and self.fetch_last_written:
            return False

        if self.rec_only and self.path:
            return False

        if self.rec_only and self.min_max:
            return False

        if self.min_max and self.checkpoint is None:
            return False

        if self.exclude_remainder and self.checkpoint is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, start):
        return MessageRequest(self.topic, start, self.end, self.path, self.fetch_last_written, self.checkpoint,
                              self.include_wrapper, self.rec_only, self.min_max, self.exclude_remainder,
                              self.backoff_limit, self.fetch_last_written_before).params()


    def change_params(self, start, end):
        return MessageRequest(self.topic, start, end, self.path, self.fetch_last_written, self.checkpoint,
                              self.include_wrapper, self.rec_only, self.min_max, self.exclude_remainder,
                              self.backoff_limit, self.fetch_last_written_before)


    def params(self):
        params = {
            self.TOPIC: self.topic,
            self.START: None if self.start is None else self.start.utc().as_iso8601(include_millis=True),
            self.END: self.end.utc().as_iso8601(include_millis=True)
        }

        if self.path is not None:
            params[self.PATH] = self.path

        if self.fetch_last_written:
            params[self.FETCH_LAST_WRITTEN] = 'true'

        if self.checkpoint is not None:
            params[self.CHECKPOINT] = self.checkpoint

        if self.include_wrapper:
            params[self.INCLUDE_WRAPPER] = 'true'

        if self.rec_only:
            params[self.REC_ONLY] = 'true'

        if self.min_max:
            params[self.MIN_MAX] = 'true'

        if self.exclude_remainder:
            params[self.EXCLUDE_REMAINDER] = 'true'

        if self.fetch_last_written_before:
            params[self.FETCH_LAST_WRITTEN_BEFORE] = 'true'

        if self.backoff_limit:
            params[self.BACKOFF_LIMIT] = self.backoff_limit

        return params


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def checkpoint(self):
        if self.__checkpoint is None:
            return None

        if self.__checkpoint == 'auto':
            return self.checkpoint_table(self.start, self.end)

        return self.__checkpoint


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def start(self):
        return self.__start


    @property
    def end(self):
        return self.__end


    @property
    def path(self):
        return self.__path


    @property
    def fetch_last_written(self):
        return self.__fetch_last_written


    @property
    def include_wrapper(self):
        return self.__include_wrapper


    @property
    def rec_only(self):
        return self.__rec_only


    @property
    def min_max(self):
        return self.__min_max


    @property
    def exclude_remainder(self):
        return self.__exclude_remainder


    @property
    def fetch_last_written_before(self):
        return self.__fetch_last_written_before


    @property
    def backoff_limit(self):
        return self.__backoff_limit


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageRequest:{topic:%s, start:%s, end:%s, path:%s, fetch_last_written:%s, checkpoint:%s, " \
               "include_wrapper:%s, rec_only:%s, min_max:%s, exclude_remainder:%s, " \
               "fetch_last_written_before:%s, backoff_limit:%s}" % \
               (self.topic, self.start, self.end, self.path, self.fetch_last_written, self.__checkpoint,
                self.include_wrapper, self.rec_only, self.min_max, self.exclude_remainder,
                self.fetch_last_written_before, self.backoff_limit)


# --------------------------------------------------------------------------------------------------------------------

class MessageResponse(APIResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        code = jdict.get('statusCode')
        status = jdict.get('status')
        fetched_last = jdict.get('fetchedLastWrittenData')
        interval = jdict.get('interval')

        items = []
        for msg_jdict in jdict.get('Items'):
            if not msg_jdict:
                continue

            item = Message.construct_from_jdict(msg_jdict) if 'payload' in msg_jdict else msg_jdict
            items.append(item)

        next_url = jdict.get('next')

        return cls(code, status, fetched_last, interval, items, next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, status, fetched_last, interval, items, next_url):
        """
        Constructor
        """
        self.__code = int(code)                         # int
        self.__status = status                          # string
        self.__fetched_last = fetched_last              # "Fetched last written data" flag
        self.__interval = interval                      # int

        self.__items = items                            # list of Message

        self.__next_url = next_url                      # URL string


    def __len__(self):
        return len(self.items)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.code is not None:
            jdict['statusCode'] = self.code

        if self.status is not None:
            jdict['status'] = self.status

        if self.fetched_last is not None:
            jdict['fetchedLastWrittenData'] = self.fetched_last

        if self.items is not None:
            jdict['interval'] = None if self.interval is None else int(round(self.interval))

            jdict['Items'] = self.items
            jdict['itemCount'] = len(self.items)

        if self.next_url is not None:
            jdict['next'] = self.next_url

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        if not self.items:
            return None

        item = self.items[0]

        try:
            return item['rec']
        except TypeError:
            return item.payload['rec']


    def end(self):
        if not self.items:
            return None

        item = self.items[-1]

        try:
            return item['rec']
        except TypeError:
            return item.payload['rec']

    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, _):
        raise NotImplemented


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    @property
    def status(self):
        return self.__status


    @property
    def fetched_last(self):
        return self.__fetched_last


    @property
    def interval(self):
        return self.__interval


    @property
    def items(self):
        return self.__items


    @property
    def next_url(self):
        return self.__next_url


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageResponse:{code:%s, status:%s, fetched_last:%s, interval:%s, items:%s, next_url:%s}" % \
               (self.code, self.status, self.fetched_last, self.interval, Str.collection(self.items), self.next_url)
