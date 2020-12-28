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
            documents = list(self.find_for_topic(topic, start_date, end_date, None, include_wrapper, False))

            if documents:
                return documents[-1]

            end_date = start_date

        return None


    def find_for_topic(self, topic, start_date, end_date, checkpoint, include_wrapper, _rec_only):
        request_path = '/default/AWSAggregate/'
        # request_path = '/topicMessages'

        params = MessageRequest(topic, start_date, end_date, include_wrapper, False, checkpoint).params()

        # request...
        self.__rest_client.connect()

        try:
            while True:
                jdict = self.__rest_client.get(request_path, params)

                # messages...
                block = MessageResponse.construct_from_jdict(jdict)

                for item in block.items:
                    yield item

                # report...
                if self.__reporter:
                    self.__reporter.print(params[self.__START], len(block))

                # next request...
                if block.next_url is None:
                    break

                next_url = urlparse(block.next_url)
                next_params = parse_qs(next_url.query)

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

    @classmethod
    def construct_from_params(cls, qsp):
        if not qsp:
            return None

        topic = qsp.get('topic')
        start = LocalizedDatetime.construct_from_iso8601(qsp.get('startTime'))
        end = LocalizedDatetime.construct_from_iso8601(qsp.get('endTime'))

        include_wrapper = qsp.get("includeWrapper", 'false') == 'true'
        min_max = qsp.get("minMax", 'false') == 'true'
        checkpoint = qsp.get('checkpoint')

        if topic is None or start is None or end is None:
            return None

        if start > end:
            return None

        return cls(topic, start, end, include_wrapper, min_max, checkpoint)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, start, end, include_wrapper, min_max, checkpoint):
        """
        Constructor
        """
        self.__topic = topic                                # string
        self.__start = start                                # LocalizedDatetime
        self.__end = end                                    # LocalizedDatetime

        self.__include_wrapper = bool(include_wrapper)      # bool
        self.__min_max = bool(min_max)                      # bool
        self.__checkpoint = checkpoint                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            'topic': self.topic,
            'startTime': self.start.utc().as_iso8601(True),
            'endTime': self.end.utc().as_iso8601(True),
            'includeWrapper': str(self.include_wrapper).lower(),
            'minMax': str(self.min_max).lower()
        }

        if self.checkpoint:
            params['checkpoint'] =  self.checkpoint

        return params


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
    def include_wrapper(self):
        return self.__include_wrapper


    @property
    def min_max(self):
        return self.__min_max


    @property
    def checkpoint(self):
        return self.__checkpoint


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageResponse:{topic:%s, start:%s, end:%s, include_wrapper:%s, min_max:%s, checkpoint:%s}" % \
               (self.topic, self.start, self.end, self.include_wrapper, self.min_max, self.checkpoint)


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

        items = []
        for msg_jdict in jdict.get('Items'):
            item = Message.construct_from_jdict(msg_jdict) if 'payload' in msg_jdict else msg_jdict
            items.append(item)

        next_url = jdict.get('next')

        return cls(code, status, items, next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, status, items, next_url):
        """
        Constructor
        """
        self.__code = Datum.int(code)               # int
        self.__status = status                      # string

        self.__items = items                        # list of Message or
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

        if self.items is not None:
            jdict['Items'] = self.items
            jdict['itemCount'] = len(self.items)

        if self.next_url is not None:
            jdict['next'] = self.next_url

        # TODO: fetched_last_written_data

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    @property
    def status(self):
        return self.__status


    @property
    def items(self):
        return self.__items


    @property
    def next_url(self):
        return self.__next_url


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageResponse:{code:%s, status:%s, items:%s, next_url:%s}" % \
               (self.code, self.status, Str.collection(self.items), self.next_url)
