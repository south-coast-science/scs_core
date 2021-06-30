"""
Created on 17 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alert example:
{"id": 123, "topic": "my/topic", "field": "my.field", "lower-threshold": 10.0, "upper-threshold": 100.0,
"alert-on-none": true, "aggregation-period": "00-01:00:00", "test-interval": "00-00:05:00",
"creator-email-address": "bruno.beloff@southcoastscience.com", "cc-list": ["bbeloff@me.com"], "suspended": false}

AlertStatus example:
{"id": 123, "rec": "2021-06-17T15:58:23Z", "cause": ">U", "value": 101.5}

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

    @classmethod
    def causes(cls):
        return [cls.BELOW_LOWER_THRESHOLD, cls.ABOVE_UPPER_THRESHOLD, cls.NULL_VALUE]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        id = jdict.get('id')

        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        cause = jdict.get('cause')
        value = jdict.get('value')

        return cls(id, rec, cause, value)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, rec, cause, value):
        """
        Constructor
        """
        self.__id = Datum.int(id)                                   # int

        self.__rec = rec                                            # LocalizedDatetime
        self.__cause = cause                                        # string
        self.__value = Datum.float(value)                           # float


    def __lt__(self, other):
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

        jdict['id'] = self.id

        jdict['rec'] = self.rec.as_iso8601()
        jdict['cause'] = self.cause
        jdict['value'] = self.value

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

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
        return "AlertStatus:{id:%s, rec:%s, cause:%s, value:%s}" %  \
               (self.id, self.rec, self.cause, self.value)


# --------------------------------------------------------------------------------------------------------------------

class Alert(JSONable):
    """
    classdocs
    """

    ID = 'id'

    TOPIC = 'topic'
    FIELD = 'field'

    LOWER_THRESHOLD = 'lowerThreshold'
    UPPER_THRESHOLD = 'upperThreshold'
    ALERT_ON_NONE = 'alertOnNone'

    AGGREGATION_PERIOD = 'aggregationPeriod'
    TEST_INTERVAL = 'testInterval'

    CREATOR_EMAIL_ADDRESS = 'creatorEmailAddress'
    CC_LIST = 'ccList.'
    SUSPENDED = 'suspended'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        id = qsp.get(cls.ID)

        topic = qsp.get(cls.TOPIC)
        field = qsp.get(cls.FIELD)

        lower_threshold = qsp.get(cls.LOWER_THRESHOLD)
        upper_threshold = qsp.get(cls.UPPER_THRESHOLD)
        alert_on_none = qsp.get(cls.ALERT_ON_NONE, 'false').lower() == 'true'

        aggregation_period = Timedelta.construct_from_jdict(qsp.get(cls.AGGREGATION_PERIOD))
        test_interval = Timedelta.construct_from_jdict(qsp.get(cls.TEST_INTERVAL))

        creator_email_address = qsp.get(cls.CREATOR_EMAIL_ADDRESS)
        cc_list = [qsp[name] for name in sorted(qsp.keys()) if name.startswith(cls.CC_LIST)]
        suspended = qsp.get(cls.SUSPENDED, 'false').lower() == 'true'

        return cls(id, topic, field, lower_threshold, upper_threshold, alert_on_none,
                   aggregation_period, test_interval, creator_email_address, cc_list, suspended)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        id = jdict.get('id')

        topic = jdict.get('topic')
        field = jdict.get('field')

        lower_threshold = jdict.get('lower-threshold')
        upper_threshold = jdict.get('upper-threshold')
        alert_on_none = jdict.get('alert-on-none')

        aggregation_period = Timedelta.construct_from_jdict(jdict.get('aggregation-period'))
        test_interval = Timedelta.construct_from_jdict(jdict.get('test-interval'))

        creator_email_address = jdict.get('creator-email-address')
        cc_list = jdict.get('cc-list')
        suspended = jdict.get('suspended')

        return cls(id, topic, field, lower_threshold, upper_threshold, alert_on_none,
                   aggregation_period, test_interval, creator_email_address, cc_list, suspended)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, topic, field, lower_threshold, upper_threshold, alert_on_none,
                 aggregation_period, test_interval, creator_email_address, cc_list, suspended):
        """
        Constructor
        """
        self.__id = Datum.int(id)                                   # int

        self.__topic = topic                                        # string topic
        self.__field = field                                        # string path

        self.__lower_threshold = Datum.float(lower_threshold)       # float                 updatable
        self.__upper_threshold = Datum.float(upper_threshold)       # float                 updatable
        self.__alert_on_none = bool(alert_on_none)                  # bool                  updatable

        self.__aggregation_period = aggregation_period              # Timedelta             updatable
        self.__test_interval = test_interval                        # Timedelta             updatable

        self.__creator_email_address = creator_email_address        # string
        self.__cc_list = cc_list                                    # array of string       updatable
        self.__suspended = bool(suspended)                          # bool                  updatable


    def __lt__(self, other):
        if self.topic < other.topic:
            return True

        if self.topic > other.topic:
            return False

        if self.field < other.field:
            return True

        if self.field > other.field:
            return False

        if self.creator_email_address < other.creator_email_address:
            return True

        if self.creator_email_address > other.creator_email_address:
            return False

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.topic is None or self.field is None or self.aggregation_period is None or \
                self.creator_email_address is None:
            return False

        if not self.has_trigger():
            return False

        if not self.has_valid_thresholds():
            return False

        return True


    def has_trigger(self):
        return self.alert_on_none or self.lower_threshold is not None or self.upper_threshold is not None


    def has_valid_thresholds(self):
        if self.lower_threshold is None or self.upper_threshold is None:
            return True

        return self.lower_threshold < self.upper_threshold


    def may_update(self, other):
        return self.id == other.id and self.topic == other.topic and self.field == other.field and \
               self.creator_email_address == other.creator_email_address


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

        return AlertStatus(self.id, LocalizedDatetime.now().utc(), cause, value)


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            self.ID: 'null' if self.id is None else self.id,
            self.TOPIC: self.topic,
            self.FIELD: self.field,
            self.AGGREGATION_PERIOD: self.aggregation_period.as_json(),
            self.CREATOR_EMAIL_ADDRESS: self.creator_email_address
        }

        if self.alert_on_none:
            params[self.ALERT_ON_NONE] = 'true'

        if self.lower_threshold is not None:
            params[self.LOWER_THRESHOLD] = self.lower_threshold

        if self.upper_threshold is not None:
            params[self.UPPER_THRESHOLD] = self.upper_threshold

        if self.test_interval is not None:
            params[self.TEST_INTERVAL] = self.test_interval.as_json()

        for i in range(len(self.cc_list)):
            params[self.CC_LIST + str(i)] = self.cc_list[i]

        if self.suspended:
            params[self.SUSPENDED] = 'true'

        return params


    def as_json(self):
        jdict = OrderedDict()

        jdict['id'] = self.id

        jdict['topic'] = self.topic
        jdict['field'] = self.field

        # note that dynamoDB does not support float - str to keep precision
        jdict['lower-threshold'] = str(self.lower_threshold)
        jdict['upper-threshold'] = str(self.upper_threshold)
        jdict['alert-on-none'] = self.alert_on_none

        jdict['aggregation-period'] = self.aggregation_period
        jdict['test-interval'] = self.test_interval

        jdict['creator-email-address'] = self.creator_email_address
        jdict['cc-list'] = self.cc_list
        jdict['suspended'] = self.suspended

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def topic(self):
        return self.__topic


    @property
    def field(self):
        return self.__field


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


    def append_to_cc_list(self, cc):
        if cc in self.__cc_list:
            return

        self.__cc_list.append(cc)


    def remove_from_cc_list(self, cc):
        if cc not in self.__cc_list:
            return

        self.__cc_list.remove(cc)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Alert:{id:%s, topic:%s, field:%s, lower_threshold:%s, upper_threshold:%s, alert_on_none:%s, " \
               "aggregation_period:%s, test_interval:%s, creator_email_address:%s, cc_list:%s, suspended:%s}" %  \
               (self.id, self.topic, self.field, self.lower_threshold, self.upper_threshold, self.alert_on_none,
                self.aggregation_period, self.test_interval, self.creator_email_address, self.cc_list, self.suspended)
