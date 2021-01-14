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
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable
from scs_core.data.str import Str
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class MessageManager(object):
    """
    classdocs
    """

    __TOPIC =               'topic'
    __START =               'startTime'
    __END =                 'endTime'
    __CHECKPOINT =          'checkpoint'
    __INCLUDE_WRAPPER =     'includeWrapper'
    __REC_ONLY =            'recOnly'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, api_key, reporter=None):
        """
        Constructor
        """
        self.__rest_client = RESTClient(api_key)
        self.__reporter = reporter


    # ----------------------------------------------------------------------------------------------------------------

    def find_latest_for_topic(self, topic, end_date, include_wrapper):
        for back_off in (1, 10, 30, 60):                            # total = 91 mins
            start_date = end_date - Timedelta(seconds=back_off)
            documents = list(self.find_for_topic(topic, start_date, end_date, False, None, include_wrapper, False))

            if documents:
                return documents[-1]

            end_date = start_date

        return None


    def find_for_topic(self, topic, start_date, end_date, fetch_last, checkpoint, include_wrapper, _rec_only):
        request_path = '/default/AWSAggregate/'
        # request_path = '/topicMessages'

        params = MessageRequest(topic, start_date, end_date, fetch_last, checkpoint, include_wrapper, False).params()
        # print("params: %s" % params)

        # request...
        self.__rest_client.connect()

        try:
            while True:
                jdict = self.__rest_client.get(request_path, params)

                # messages...
                block = MessageResponse.construct_from_jdict(jdict)
                # print("block: %s" % block)

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
                params[self.__START] = next_params[self.__START][0]

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
            return '/01:00:00'

        return '/06:00:00'


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        topic = qsp.get('topic')
        start = LocalizedDatetime.construct_from_iso8601(qsp.get('startTime'))
        end = LocalizedDatetime.construct_from_iso8601(qsp.get('endTime'))

        include_wrapper = qsp.get("includeWrapper", 'false') == 'true'
        min_max = qsp.get("minMax", 'false') == 'true'
        fetch_last_written = qsp.get("fetchLastWrittenData", 'false') == 'true'
        checkpoint = qsp.get('checkpoint')

        if topic is None or start is None or end is None:
            return None

        if start > end:
            return None

        return cls(topic, start, end, fetch_last_written, checkpoint, include_wrapper, min_max)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, start, end, fetch_last_written, checkpoint, include_wrapper, min_max):
        """
        Constructor
        """
        self.__topic = topic                                # string
        self.__start = start                                # LocalizedDatetime
        self.__end = end                                    # LocalizedDatetime

        self.__fetch_last_written = fetch_last_written      # bool or None

        self.__checkpoint = checkpoint                      # string
        self.__include_wrapper = bool(include_wrapper)      # bool
        self.__min_max = bool(min_max)                      # bool


    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, start):
        return MessageRequest(self.topic, start, self.end, self.fetch_last_written, self.checkpoint,
                              self.include_wrapper, self.min_max).params()


    def params(self):
        params = {
            'topic': self.topic,
            'startTime': self.start.utc().as_iso8601(include_millis=True),
            'endTime': self.end.utc().as_iso8601(include_millis=True),
            'includeWrapper': str(self.include_wrapper).lower(),
            'minMax': str(self.min_max).lower(),
        }

        if self.checkpoint is not None:
            params['checkpoint'] =  self.__checkpoint

        if self.fetch_last_written:
            params['fetchLastWrittenData'] =  str(self.fetch_last_written).lower()

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
    def min_max(self):
        return self.__min_max


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageRequest:{topic:%s, start:%s, end:%s, fetch_last_written:%s, checkpoint:%s, " \
               "include_wrapper:%s, min_max:%s}" % \
               (self.topic, self.start, self.end, self.fetch_last_written, self.__checkpoint,
                self.include_wrapper, self.min_max)


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

        items = []
        for msg_jdict in jdict.get('Items'):
            item = Message.construct_from_jdict(msg_jdict) if 'payload' in msg_jdict else msg_jdict
            items.append(item)

        next_url = jdict.get('next')

        return cls(code, status, fetched_last, items, next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, status, fetched_last, items, next_url):
        """
        Constructor
        """
        self.__code = Datum.int(code)               # int
        self.__status = status                      # string
        self.__fetched_last = fetched_last          # Fetched last written data flag

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
            jdict['Items'] = self.items
            jdict['itemCount'] = len(self.items)

        if self.next_url is not None:
            jdict['next'] = self.next_url

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        if not self.items:
            return None

        return self.items[0].get('rec')


    def end(self):
        if not self.items:
            return None

        return self.items[len(self) - 1].get('rec')


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
    def items(self):
        return self.__items


    @property
    def next_url(self):
        return self.__next_url


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageResponse:{code:%s, status:%s, fetched_last:%s, items:%s, next_url:%s}" % \
               (self.code, self.status, self.fetched_last, Str.collection(self.items), self.next_url)
