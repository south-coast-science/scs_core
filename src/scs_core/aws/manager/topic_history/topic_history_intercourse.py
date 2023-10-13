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
from urllib.parse import parse_qs, urlparse

from scs_core.aws.client.api_intercourse import APIResponse
from scs_core.aws.data.message import Message

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.str import Str
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class TopicHistoryRequest(object):
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
        return TopicHistoryRequest(self.topic, start, self.end, self.path, self.fetch_last_written, self.checkpoint,
                                   self.include_wrapper, self.rec_only, self.min_max, self.exclude_remainder,
                                   self.backoff_limit, self.fetch_last_written_before).params()


    def change_params(self, start, end):
        return TopicHistoryRequest(self.topic, start, end, self.path, self.fetch_last_written, self.checkpoint,
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
        return "TopicHistoryRequest:{topic:%s, start:%s, end:%s, path:%s, fetch_last_written:%s, checkpoint:%s, " \
               "include_wrapper:%s, rec_only:%s, min_max:%s, exclude_remainder:%s, " \
               "fetch_last_written_before:%s, backoff_limit:%s}" % \
               (self.topic, self.start, self.end, self.path, self.fetch_last_written, self.__checkpoint,
                self.include_wrapper, self.rec_only, self.min_max, self.exclude_remainder,
                self.fetch_last_written_before, self.backoff_limit)


# --------------------------------------------------------------------------------------------------------------------

class TopicHistoryResponse(APIResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        fetched_last = jdict.get('fetchedLastWrittenData')
        interval = jdict.get('interval')

        items = []
        for msg_jdict in jdict.get('Items'):
            item = Message.construct_from_jdict(msg_jdict) if 'payload' in msg_jdict else msg_jdict
            items.append(item)

        next_url = jdict.get('next')

        return cls(fetched_last, interval, items, next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, fetched_last, interval, items, next_url):
        """
        Constructor
        """
        self.__fetched_last = fetched_last                      # "Fetched last written data" flag
        self.__interval = interval                              # int

        self.__items = items                                    # list of Message

        self.__next_url = next_url                              # URL string


    def __len__(self):
        return len(self.items)


    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, params):
        return parse_qs(urlparse(self.next_url).query)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

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
        return "TopicHistoryResponse:{fetched_last:%s, interval:%s, items:%s, next_url:%s}" % \
               (self.fetched_last, self.interval, Str.collection(self.items), self.next_url)
