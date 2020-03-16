"""
Created on 13 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

import urllib.parse

from scs_core.data.datetime import LocalizedDatetime

from scs_core.osio.client.rest_client import RESTClient
from scs_core.osio.data.message import Message


# --------------------------------------------------------------------------------------------------------------------

class MessageManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, api_key, verbose=False):
        """
        Constructor
        """
        self.__rest_client = RESTClient(http_client, api_key)
        self.__verbose = verbose


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_topic(self, topic, start_date, end_date, batch_pause=0.0):
        request_path = '/v1/messages/topic/' + topic

        total = 0
        collection = []

        # request...
        self.__rest_client.connect()

        try:
            for batch in self.__find(request_path, start_date, end_date):
                collection.extend(batch)

                if self.__verbose:
                    now = LocalizedDatetime.now().utc()
                    batch_count = len(batch)
                    total += batch_count

                    print("%s: batch: %d total: %d" % (now.as_iso8601(), batch_count, total), file=sys.stderr)
                    sys.stderr.flush()

                time.sleep(batch_pause)     # prevent "Rate limit exceeded" error

        finally:
            self.__rest_client.close()

        return collection


    # ----------------------------------------------------------------------------------------------------------------

    def __find(self, request_path, start_date, end_date):
        params = {'start-date': start_date.as_iso8601(), 'end-date': end_date.as_iso8601()}

        while True:
            # request...
            jdict = self.__rest_client.get(request_path, params)

            # messages...
            msgs_jdict = jdict.get('messages')
            messages = [Message.construct_from_jdict(msg_jdict) for msg_jdict in msgs_jdict] if msgs_jdict else []

            yield messages

            # next...
            next_jdict = jdict.get('next')
            next_query = NextMessageQuery.construct_from_uri(next_jdict)

            if next_query is None:
                return

            params['start-date'] = next_query.start_date.as_iso8601()
            params['end-date'] = next_query.end_date.as_iso8601()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageManager:{rest_client:%s, verbose:%s}" % (self.__rest_client, self.__verbose)


# --------------------------------------------------------------------------------------------------------------------

class NextMessageQuery(object):
    """
    classdocs

    example query:
    /v1/messages/topic//users/southcoastscience-dev/test/json?
    start-date=2016-11-13T07:11:14.779Z&end-date=2016-11-13T08:48:08.901+00:00
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_uri(cls, uri):
        if not uri:
            return None

        # parse...
        parse = urllib.parse.urlparse(urllib.parse.unquote(uri))
        params = urllib.parse.parse_qs(parse[4])

        if 'start-date' not in params or 'end-date' not in params:
            return None

        # construct...
        start_date = LocalizedDatetime.construct_from_iso8601(params['start-date'][0])
        end_date = LocalizedDatetime.construct_from_iso8601(params['end-date'][0])

        if not start_date or not end_date:
            return None

        return NextMessageQuery(start_date, end_date)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, start_date, end_date):
        """
        Constructor
        """
        self.__start_date = start_date          # LocalizedDatetime
        self.__end_date = end_date              # LocalizedDatetime


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def start_date(self):
        return self.__start_date


    @property
    def end_date(self):
        return self.__end_date


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NextMessageQuery:{start_date:%s, end_date:%s}" % (self.start_date, self.end_date)
