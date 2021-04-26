"""
Created on 26 Nov 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

This version of MessageManager for AWS lambda function with multi-part response.

Equivalent to cURL:
curl "https://aws.southcoastscience.com/topicMessages?topic=unep/ethiopia/loc/1/climate
&startTime=2018-12-13T07:03:59.712Z&endTime=2018-12-13T15:10:59.712Z"
"""

from collections import OrderedDict
from urllib.parse import urlparse, parse_qs

from scs_core.aws.client.rest_client import RESTClient
from scs_core.aws.data.message import Message

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.str import Str
from scs_core.data.timedelta import Timedelta

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class MessageManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, api_key, reporter=None):
        """
        Constructor
        """
        self.__rest_client = RESTClient(api_key)
        self.__reporter = reporter

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def find_latest_for_topic(self, topic, end, include_wrapper, rec_only):
        for back_off in (1, 10, 30, 60):
            start = end - Timedelta(seconds=back_off)
            documents = list(self.find_for_topic(topic, start, end, False, None, include_wrapper, rec_only,
                                                 False, False))

            if documents:
                return documents[-1]

            end = start

        return None


    def find_for_topic(self, topic, start, end, fetch_last, checkpoint, include_wrapper, rec_only,
                       min_max, exclude_remainder):
        request_path = '/topicMessages'

        request = MessageRequest(topic, start, end, fetch_last, checkpoint, include_wrapper, rec_only,
                                 min_max, exclude_remainder)
        self.__logger.debug(request)

        params = request.params()

        # request...
        self.__rest_client.connect()

        try:
            while True:
                jdict = self.__rest_client.get(request_path, params)

                # messages...
                block = MessageResponse.construct_from_jdict(jdict)
                self.__logger.debug(block)

                for item in block.items:
                    yield item

                # report...
                if self.__reporter:
                    self.__reporter.print(block.start(), len(block))

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
        return "MessageManager:{rest_client:%s, reporter:%s}" % (self.__rest_client, self.__reporter)


# --------------------------------------------------------------------------------------------------------------------

class MessageRequest(object):
    """
    classdocs
    """

    TOPIC = 'topic'
    START = 'startTime'
    END = 'endTime'
    FETCH_LAST_WRITTEN = 'fetchLastWrittenData'
    CHECKPOINT = 'checkpoint'
    INCLUDE_WRAPPER = 'includeWrapper'
    REC_ONLY = 'recOnly'
    MIN_MAX = 'minMax'
    EXCLUDE_REMAINDER = 'excludeRemainder'

    # ----------------------------------------------------------------------------------------------------------------

    __DAY = Timedelta(days=1)
    __WEEK = Timedelta(weeks=1)
    __MONTH = Timedelta(days=28)
    __YEAR = Timedelta(days=365)

    @classmethod
    def checkpoint_table(cls, start, end):
        delta = end - start

        if delta < cls.__DAY:
            return None             # raw data rate

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
        fetch_last_written = qsp.get(cls.FETCH_LAST_WRITTEN, 'false').lower() == 'true'
        checkpoint = qsp.get(cls.CHECKPOINT)
        include_wrapper = qsp.get(cls.INCLUDE_WRAPPER, 'false').lower() == 'true'
        rec_only = qsp.get(cls.REC_ONLY, 'false').lower() == 'true'
        min_max = qsp.get(cls.MIN_MAX, 'false').lower() == 'true'
        exclude_remainder = qsp.get(cls.EXCLUDE_REMAINDER, 'false').lower() == 'true'

        if checkpoint and checkpoint.lower() == 'none':
            checkpoint = None

        return cls(topic, start, end, fetch_last_written, checkpoint, include_wrapper, rec_only,
                   min_max, exclude_remainder)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, start, end, fetch_last_written, checkpoint, include_wrapper, rec_only,
                 min_max, exclude_remainder):
        """
        Constructor
        """
        self.__topic = topic                                        # string
        self.__start = start                                        # LocalizedDatetime
        self.__end = end                                            # LocalizedDatetime

        self.__fetch_last_written = bool(fetch_last_written)        # bool
        self.__checkpoint = checkpoint                              # string
        self.__include_wrapper = bool(include_wrapper)              # bool
        self.__rec_only = bool(rec_only)                            # bool
        self.__min_max = bool(min_max)                              # bool
        self.__exclude_remainder = bool(exclude_remainder)          # bool


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

        if self.rec_only and self.min_max:
            return False

        if self.min_max and self.checkpoint is None:
            return False

        if self.exclude_remainder and self.checkpoint is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, start):
        return MessageRequest(self.topic, start, self.end, self.fetch_last_written, self.checkpoint,
                              self.include_wrapper, self.rec_only, self.min_max, self.exclude_remainder).params()


    def change_params(self, start, end):
        return MessageRequest(self.topic, start, end, self.fetch_last_written, self.checkpoint,
                              self.include_wrapper, self.rec_only, self.min_max, self.exclude_remainder)


    def params(self):
        params = {
            self.TOPIC: self.topic,
            self.START: self.start.utc().as_iso8601(include_millis=True),
            self.END: self.end.utc().as_iso8601(include_millis=True)
        }

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


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageRequest:{topic:%s, start:%s, end:%s, fetch_last_written:%s, checkpoint:%s, " \
               "include_wrapper:%s, rec_only:%s, min_max:%s, exclude_remainder:%s}" % \
               (self.topic, self.start, self.end, self.fetch_last_written, self.__checkpoint,
                self.include_wrapper, self.rec_only, self.min_max, self.exclude_remainder)


# --------------------------------------------------------------------------------------------------------------------

class MessageResponse(JSONable):
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
            item = Message.construct_from_jdict(msg_jdict) if 'payload' in msg_jdict else msg_jdict
            items.append(item)

        next_url = jdict.get('next')

        return cls(code, status, fetched_last, interval, items, next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, status, fetched_last, interval, items, next_url):
        """
        Constructor
        """
        self.__code = int(code)                     # int
        self.__status = status                      # string
        self.__fetched_last = fetched_last          # Fetched last written data flag
        self.__interval = interval                  # int

        self.__items = items                        # list of Message

        self.__next_url = next_url                  # URL string


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
