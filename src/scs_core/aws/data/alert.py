"""
Created on 17 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alert example:
{"topic": "my/topic", "field": "my.field", "id": 123, "lower-threshold": 10.0, "upper-threshold": 100.0,
"alert-on-none": true, "aggregation-period": "00-01:00:00", "test-interval": "00-00:05:00",
"creator-email-address": "bruno.beloff@southcoastscience.com", "cc-list": ["bbeloff@me.com"], "is-suspended": false}

AlertStatus example:
{"topic": "my/topic", "field": "my.field", "id": 123, "rec": "2021-06-17T15:58:23Z", "cause": ">U", "value": 101.5}

https://martinstapel.com/how-to-autoincrement-in-dynamo-db-if-you-really-need-to/
https://stackoverflow.com/questions/37072341/how-to-use-auto-increment-for-primary-key-id-in-dynamodb
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class AlertStatus(JSONable):
    """
    classdocs
    """

    BELOW_LOWER_THRESHOLD =     '<L'
    ABOVE_UPPER_THRESHOLD =     '>U'
    NULL_VALUE =                'NV'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        topic = jdict.get('topic')
        field = jdict.get('field')
        id = jdict.get('id')

        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        cause = jdict.get('cause')
        value = jdict.get('value')

        return cls(topic, field, id, rec, cause, value)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, field, id, rec, cause, value):
        """
        Constructor
        """
        self.__topic = topic                                        # string topic
        self.__field = field                                        # string path
        self.__id = Datum.int(id)                                   # int

        self.__rec = rec                                            # LocalizedDatetime
        self.__cause = cause                                        # string
        self.__value = Datum.float(value)                           # float


    def __lt__(self, other):
        if self.topic < other.topic:
            return True

        if self.topic > other.topic:
            return False

        if self.field < other.field:
            return True

        if self.field > other.field:
            return False

        if self.id < other.id:
            return True

        if self.id > other.id:
            return False

        if self.rec < other.rec:
            return True

        if self.rec > other.rec:
            return False

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def is_excursion(self):
        return self.cause is not None


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['topic'] = self.topic
        jdict['field'] = self.field
        jdict['id'] = self.id

        jdict['rec'] = self.rec.as_iso8601()
        jdict['cause'] = self.cause
        jdict['value'] = self.value

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def field(self):
        return self.__field


    @property
    def id(self):
        return self.__id


    @property
    def rec(self):
        return self.__rec


    @property
    def cause(self):
        return self.__cause


    @property
    def value(self):
        return self.__value


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AlertStatus:{topic:%s, field:%s, id:%s, rec:%s, cause:%s, value:%s}" %  \
               (self.topic, self.field, self.id, self.rec, self.cause, self.value)


# --------------------------------------------------------------------------------------------------------------------

class Alert(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        topic = jdict.get('topic')
        field = jdict.get('field')
        id = jdict.get('id')

        lower_threshold = jdict.get('lower-threshold')
        upper_threshold = jdict.get('upper-threshold')
        alert_on_none = jdict.get('alert-on-none')

        aggregation_period = Timedelta.construct_from_jdict(jdict.get('aggregation-period'))
        test_interval = Timedelta.construct_from_jdict(jdict.get('test-interval'))

        creator_email_address = jdict.get('creator-email-address')
        cc_list = jdict.get('cc-list')
        suspended = jdict.get('is-suspended')

        return cls(topic, field, id, lower_threshold, upper_threshold, alert_on_none,
                   aggregation_period, test_interval, creator_email_address, cc_list, suspended)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, field, id, lower_threshold, upper_threshold, alert_on_none,
                 aggregation_period, test_interval, creator_email_address, cc_list, suspended):
        """
        Constructor
        """
        self.__topic = topic                                        # string topic
        self.__field = field                                        # string path
        self.__id = Datum.int(id)                                   # int

        self.__lower_threshold = Datum.float(lower_threshold)       # float
        self.__upper_threshold = Datum.float(upper_threshold)       # float
        self.__alert_on_none = bool(alert_on_none)                  # bool

        self.__aggregation_period = aggregation_period              # Timedelta
        self.__test_interval = test_interval                        # Timedelta

        self.__creator_email_address = creator_email_address        # string
        self.__cc_list = cc_list                                    # array of string
        self.__suspended = bool(suspended)                          # bool


    def __lt__(self, other):
        if self.topic < other.topic:
            return True

        if self.topic > other.topic:
            return False

        if self.field < other.field:
            return True

        if self.field > other.field:
            return False

        if self.id < other.id:
            return True

        if self.id > other.id:
            return False

        if self.creator_email_address < other.creator_email_address:
            return True

        if self.creator_email_address > other.creator_email_address:
            return False

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def status(self, value):
        if self.suspended:
            return None

        if value is None and self.alert_on_none:
            cause = AlertStatus.NULL_VALUE

        elif self.lower_threshold is not None and value is not None and value < self.lower_threshold:
            cause = AlertStatus.BELOW_LOWER_THRESHOLD

        elif self.upper_threshold is not None and value is not None and value > self.upper_threshold:
            cause = AlertStatus.ABOVE_UPPER_THRESHOLD

        else:
            cause = None

        return AlertStatus(self.topic, self.field, self.id, LocalizedDatetime.now().utc(), cause, value)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['topic'] = self.topic
        jdict['field'] = self.field
        jdict['id'] = self.id

        jdict['lower-threshold'] = self.lower_threshold
        jdict['upper-threshold'] = self.upper_threshold
        jdict['alert-on-none'] = self.alert_on_none

        jdict['aggregation-period'] = self.aggregation_period
        jdict['test-interval'] = self.test_interval

        jdict['creator-email-address'] = self.creator_email_address
        jdict['cc-list'] = self.cc_list
        jdict['is-suspended'] = self.suspended

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def field(self):
        return self.__field


    @property
    def id(self):
        return self.__id


    @property
    def lower_threshold(self):
        return self.__lower_threshold


    @property
    def upper_threshold(self):
        return self.__upper_threshold


    @property
    def alert_on_none(self):
        return self.__alert_on_none


    @property
    def aggregation_period(self):
        return self.__aggregation_period


    @property
    def test_interval(self):
        return self.__test_interval


    @property
    def creator_email_address(self):
        return self.__creator_email_address


    @property
    def cc_list(self):
        return self.__cc_list


    @property
    def suspended(self):
        return self.__suspended


    # ----------------------------------------------------------------------------------------------------------------

    @id.setter
    def id(self, id):
        self.__id = id


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Alert:{topic:%s, field:%s, id:%s, lower_threshold:%s, upper_threshold:%s, alert_on_none:%s, " \
               "aggregation_period:%s, test_interval:%s, creator_email_address:%s, cc_list:%s, suspended:%s}" %  \
               (self.topic, self.field, self.id, self.lower_threshold, self.upper_threshold, self.alert_on_none,
                self.aggregation_period, self.test_interval, self.creator_email_address, self.cc_list, self.suspended)
