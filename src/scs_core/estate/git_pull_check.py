"""
Created on 24 May 2021

@author: Jade Page (jade.page@southcoastscience.com)

document example:
{"tag": "scs-bgx-003", "rec": "2021-04-14T08:49:22+01:00", "result": "PENDING"}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class GitPullCheck(JSONable):
    """
    classdocs
    """

    RESULT_PENDING =                    "PENDING"
    RESULT_ERROR =                      "ERROR"
    RESULT_DONE =                       "DONE"
    RESULT_NOT_SUPPORTED =              "NOT SUPPORTED"
    RESULT_MALFORMED_GIT_PULL =         "MALFORMED:GIT_PULL"

    __RESULTS = {
        'PEN': RESULT_PENDING,
        'ERR': RESULT_ERROR,
        'NSP': RESULT_NOT_SUPPORTED,
        'MGP': RESULT_MALFORMED_GIT_PULL,
        'D':   RESULT_DONE
    }

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def result_codes(cls):
        return cls.__RESULTS.keys()


    @classmethod
    def result_string(cls, code):
        if code is None:
            return None

        return cls.__RESULTS[code]


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        tag = jdict.get('tag')
        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        message_rec = LocalizedDatetime.construct_from_iso8601(jdict.get('message-rec'))
        result = jdict.get('result')
        context = jdict.get('context')

        return cls(tag, rec, message_rec, result, context=context)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, message_rec, result, context=''):
        """
        Constructor
        """
        self.__tag = tag                        # string
        self.__rec = rec                        # LocalizedDatetime - when this record was created
        self.__message_rec = message_rec        # LocalizedDatetime - the rec of the ControlReceipt
        self.__result = result                  # string
        self.__context = context                # string (only for ERROR)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['rec'] = self.rec.as_iso8601()
        jdict['message-rec'] = None if self.message_rec is None else self.message_rec.as_iso8601()
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
    def message_rec(self):
        return self.__message_rec


    @property
    def result(self):
        return self.__result

    @property
    def context(self):
        return self.__context


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GitPullCheck:{tag:%s, rec:%s, message_rec:%s, result:%s, context:%s}" % \
               (self.tag, self.rec, self.message_rec, self.result, self.context)
