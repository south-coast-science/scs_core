'''
Created on 10 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"date": "2016-11-19T20:31:16.563+00:00", "payload": {"encoding": "utf-8", "content-type": "application/json", "text": "{\"rec\": \"2016-11-19T20:31:23.882+00:00\", \"val\": {\"host\": {\"tmp\": 46.2}}}"}}

'''

from collections import OrderedDict

from scs_core.common.json import JSONable
from scs_core.common.localized_datetime import LocalizedDatetime

from scs_core.osio.data.message_payload import MessagePayload


# TODO: how should we distinguish between HTTP and MQTT topic clients? unification here?

# --------------------------------------------------------------------------------------------------------------------

class Message(JSONable):
    '''
    classdocs
   '''

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def find_for_topic(cls, http_client, api_key, topic, start_date, end_date):     # TODO: use auth, not api_key
        finder = MessageFinder(http_client, api_key)

        return finder.find_for_topic(topic, start_date, end_date)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        date = LocalizedDatetime.construct_from_iso8601(jdict.get('date'))
        payload = MessagePayload.construct_from_jdict(jdict.get('payload'))

        return Message(date, payload)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, date, payload):
        '''
        Constructor
        '''
        self.__date = date                    # LocalizedDatetime
        self.__payload = payload              # MessagePayload


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['date'] = self.date
        jdict['payload'] = self.payload

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def date(self):
        return self.__date


    @property
    def payload(self):
        return self.__payload


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Message:{date:%s, payload:%s}" % (self.date, self.payload)


# --------------------------------------------------------------------------------------------------------------------

from scs_core.osio.finder.message_finder import MessageFinder
