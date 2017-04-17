"""
Created on 17 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://pythoncentral.io/hashing-strings-with-python/
"""

import hashlib

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class ControlReceipt(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        tag = jdict.get('tag')
        date = LocalizedDatetime.construct_from_iso8601(jdict.get('date'))
        omd = jdict.get('omd')
        digest = jdict.get('digest')

        datum = ControlReceipt(tag, date, omd, digest)

        return datum


    @classmethod
    def construct_from_datum(cls, datum, date, subscriber_sn):
        digest = ControlReceipt.__hash(datum.tag, date, datum.digest, subscriber_sn)

        return ControlReceipt(datum.tag, date, datum.digest, digest)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __hash(cls, tag, date, omd, subscriber_sn):
        text = str(tag) + date.as_json() + str(omd) + str(subscriber_sn)
        hash_object = hashlib.sha256(text.encode())

        return hash_object.hexdigest()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, date, omd, digest):
        """
        Constructor
        """
        self.__tag = tag                # string
        self.__date = date              # LocalizedDatetime
        self.__omd = omd                # string
        self.__digest = digest          # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self, subscriber_sn):
        digest = ControlReceipt.__hash(self.tag, self.date, self.omd, subscriber_sn)

        return digest == self.__digest


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['date'] = self.date
        jdict['omd'] = self.omd
        jdict['digest'] = self.__digest

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def date(self):
        return self.__date


    @property
    def omd(self):
        return self.__omd


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ControlReceipt:{tag:%s, date:%s, omd:%s, digest:%s}" % \
               (self.tag, self.date, self.omd, self.__digest)
