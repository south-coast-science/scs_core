"""
Created on 14 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"tag": "scs-bgx-003", "rec": "2021-04-14T08:49:22+01:00", "result": "ERROR", "context": "stderr output"}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCheck(JSONable):
    """
    classdocs
    """

    RESULT_NO_RESPONSE =                "NO RESPONSE"
    RESULT_ERROR =                      "ERROR"
    RESULT_MALFORMED =                  "MALFORMED:"
    RESULT_MALFORMED_SAMPLE =           "MALFORMED:SAMPLE"
    RESULT_MALFORMED_CONFIG =           "MALFORMED:CONFIG"
    RESULT_NOT_SUPPORTED =              "NOT SUPPORTED"
    RESULT_RECEIVED =                   "RECEIVED:"
    RESULT_RECEIVED_NEW =               "RECEIVED:NEW"
    RESULT_RECEIVED_UNCHANGED =         "RECEIVED:UNCHANGED"
    RESULT_RECEIVED_UPDATED =           "RECEIVED:UPDATED"

    __RESULTS = {
        'NOR': RESULT_NO_RESPONSE,
        'ERR': RESULT_ERROR,
        'M': RESULT_MALFORMED,
        'MSA': RESULT_MALFORMED_SAMPLE,
        'MCO': RESULT_MALFORMED_CONFIG,
        'NSP': RESULT_NOT_SUPPORTED,
        'R': RESULT_RECEIVED,
        'RNW': RESULT_RECEIVED_NEW,
        'RUN': RESULT_RECEIVED_UNCHANGED,
        'RUP': RESULT_RECEIVED_UPDATED
    }

    @classmethod
    def result_codes(cls):
        return cls.__RESULTS.keys()


    @classmethod
    def result_string(cls, code):
        if code is None:
            return None

        return cls.__RESULTS[code]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        tag = jdict.get('tag')
        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        result = jdict.get('result')
        context = jdict.get('context')

        return cls(tag, rec, result, context)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, result, context=''):
        """
        Constructor
        """
        self.__tag = tag                        # string
        self.__rec = rec                        # LocalizedDatetime
        self.__result = result                  # string
        self.__context = context                # string (only for MALFORMED or ERROR)


    def __lt__(self, other):
        if self.tag < other.tag:
            return True

        if self.tag > other.tag:
            return False

        if self.rec < other.rec:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['rec'] = self.rec.as_iso8601()
        jdict['result'] = self.result
        jdict['context'] = self.context if self.context else ["-"]

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def rec(self):
        return self.__rec


    @property
    def result(self):
        return self.__result


    @property
    def context(self):
        return self.__context


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationCheck:{tag:%s, rec:%s, result:%s, context:%s}" % \
               (self.tag, self.rec, self.result, self.context)
