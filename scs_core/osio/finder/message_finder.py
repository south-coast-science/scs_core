'''
Created on 13 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

deliver-change
870725f3-e692-4538-aa81-bfa8b51d44e7

south-coast-science-dev
43308b72-ad41-4555-b075-b4245c1971db
'''

import urllib.parse

from scs_core.common.localized_datetime import LocalizedDatetime

from scs_core.osio.client.rest_client import RESTClient

from scs_core.osio.data.message import Message


# --------------------------------------------------------------------------------------------------------------------

class MessageFinder(object):
    '''
    classdocs
    '''

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, api_key):
        '''
        Constructor
        '''
        self.__rest_client = RESTClient(http_client, api_key)


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_topic(self, topic, start_date, end_date):
        path = '/v1/messages/topic/' + topic

        self.__rest_client.connect()

        collection = []

        for messages in self.__get(path, start_date, end_date):
            collection.extend(messages)

        self.__rest_client.close()

        return collection


    # ----------------------------------------------------------------------------------------------------------------

    def __get(self, path, start_date, end_date):
        params = { 'start-date': start_date.as_iso8601(), 'end-date': end_date.as_iso8601() }

        while True:
            # request...
            jdict = self.__rest_client.get(path, params)

            # messages...
            msg_jdict = jdict.get('messages')
            messages = [Message.construct_from_jdict(msg_jdict) for msg_jdict in msg_jdict] if msg_jdict else []

            yield (messages)

            # next...
            next_jdict = jdict.get('next')
            next = NextMessageQuery.construct_from_uri(next_jdict)

            if not next:
                return

            params['start-date'] = next.start_date.as_iso8601()
            params['end-date'] = next.end_date.as_iso8601()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageFinder:{rest_client:%s}" % self.__rest_client


# --------------------------------------------------------------------------------------------------------------------

class NextMessageQuery(object):
    '''
    classdocs

    example query:
    /v1/messages/topic//users/southcoastscience-dev/test/json?start-date=2016-11-13T07:11:14.779Z&end-date=2016-11-13T08:48:08.901+00:00
    '''

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_uri(cls, uri):
        if not uri:
            return None

        # parse...
        parse = urllib.parse.urlparse(urllib.parse.unquote(uri))
        params = urllib.parse.parse_qs(parse[4])

        if not 'start-date' in params or not 'end-date' in params:
            return None

        # construct...
        start_date = LocalizedDatetime.construct_from_iso8601(params['start-date'][0])
        end_date = LocalizedDatetime.construct_from_iso8601(params['end-date'][0])

        if not start_date or not end_date:
            return None

        return NextMessageQuery(start_date, end_date)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, start_date, end_date):
        '''
        Constructor
        '''
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
