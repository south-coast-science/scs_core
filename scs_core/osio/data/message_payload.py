'''
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"encoding": "utf-8", "content-type": "application/json", "text": "{\"rec\": \"2016-11-19T20:31:23.882+00:00\", \"val\": {\"host\": {\"tmp\": 46.2}}}"}}
'''

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class MessagePayload(JSONable):
    '''
    classdocs
   '''

    __TYPE_JSON =       'application/json'
    __TYPE_TEXT =       'text/plain'


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        encoding = jdict.get('encoding')
        content_type = jdict.get('content-type')
        text = jdict.get('text')

        payload = PathDict.construct_from_jstr(text) if content_type == cls.__TYPE_JSON else text

        return MessagePayload(encoding, content_type, payload)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, encoding, content_type, payload):
        '''
        Constructor
        '''
        self.__encoding = encoding              # string			utf-8
        self.__content_type = content_type      # string			application/json

        self.__payload = payload                # string			JSON document


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['encoding'] = self.encoding
        jdict['content-type'] = self.content_type

        jdict['payload'] = self.payload

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def encoding(self):
        return self.__encoding


    @property
    def content_type(self):
        return self.__content_type


    @property
    def payload(self):
        return self.__payload


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessagePayload:{encoding:%s, content_type:%s, payload:%s}" % (self.encoding, self.content_type, self.payload)
