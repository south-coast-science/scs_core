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

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable, JSONify
from scs_core.data.str import Str
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class MessageManager(object):
    """
    classdocs
    """

    __TOPIC =       'topic'
    __START =       'startTime'
    __END =         'endTime'
    __REC_ONLY =    'rec_only'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, api_key, reporter=None):
        """
        Constructor
        """
        self.__rest_client = RESTClient(api_key)
        self.__reporter = reporter


    # ----------------------------------------------------------------------------------------------------------------

    def find_latest_for_topic(self, topic, end_date):
        for back_off in (1, 10, 30, 60):                            # total = 91 mins
            start_date = end_date - Timedelta(seconds=back_off)
            documents = list(self.find_for_topic(topic, start_date, end_date, False))

            if documents:
                return documents[-1]

            end_date = start_date

        return None


    def find_for_topic(self, topic, start_date, end_date, rec_only):
        # request_path = '/default/AWSAggregate/'
        request_path = '/topicMessages'

        params = {self.__TOPIC:     topic,
                  self.__START:     start_date.utc().as_iso8601(True),
                  self.__END:       end_date.utc().as_iso8601(True),
                  self.__REC_ONLY:  str(rec_only).lower()}

        # 'checkpoint':     '**:/15:00'}
        # self.__REC_ONLY:  str(rec_only).lower()}


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

class MessageResponse(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        print("jdict: %s" % jdict)

        code = jdict.get('statusCode')
        status = jdict.get('status')

        items = [Message.construct_from_jdict(msg_jdict) for msg_jdict in jdict.get('Items')]
        next_url = jdict.get('next')

        return MessageResponse(code, status, items, next_url)


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

        if self.next_url is not None:
            jdict['next'] = self.next_url

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
