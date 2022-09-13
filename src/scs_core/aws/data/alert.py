"""
Created on 17 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alert example:
{"id": 77, "topic": "south-coast-science-dev/development/loc/1/gases", "field": "val.CO.cnc", "lower-threshold": null,
"upper-threshold": 1000.0, "alert-on-none": true, "aggregation-period": {"interval": 1, "units": "M"},
"test-interval": null, "creator-email-address": "authorization@southcoastscience.com",
"to": "someone@me.com", "cc-list": [], "suspended": false}

AlertStatus example:
{"id": 77, "rec": "2021-09-07T11:40:00Z", "cause": null, "val": 589.6}

https://martinstapel.com/how-to-autoincrement-in-dynamo-db-if-you-really-need-to/
https://stackoverflow.com/questions/37072341/how-to-use-auto-increment-for-primary-key-id-in-dynamodb
"""

from collections import OrderedDict

from scs_core.data.recurring_period import RecurringPeriod
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


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
        return cls.BELOW_LOWER_THRESHOLD, cls.ABOVE_UPPER_THRESHOLD, cls.NULL_VALUE


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        id = jdict.get('id')

        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        cause = jdict.get('cause')
        value = jdict.get('val')

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

        jdict['rec'] = self.rec
        jdict['cause'] = self.cause
        jdict['val'] = self.value

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

class AlertSpecification(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

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

        aggregation_period = RecurringPeriod.construct_from_jdict(jdict.get('aggregation-period'))
        test_interval = RecurringPeriod.construct_from_jdict(jdict.get('test-interval'))

        creator_email_address = jdict.get('creator-email-address')

        to = jdict.get('to')
        cc_list = jdict.get('cc-list')
        suspended = jdict.get('suspended')

        return cls(id, topic, field, lower_threshold, upper_threshold, alert_on_none,
                   aggregation_period, test_interval, creator_email_address, to, cc_list, suspended)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, topic, field, lower_threshold, upper_threshold, alert_on_none,
                 aggregation_period, test_interval, creator_email_address, to, cc_list, suspended):
        """
        Constructor
        """
        self.__id = Datum.int(id)                                   # int

        self.__topic = topic                                        # string topic
        self.__field = field                                        # string path

        self.__lower_threshold = Datum.float(lower_threshold)       # float                 updatable
        self.__upper_threshold = Datum.float(upper_threshold)       # float                 updatable
        self.__alert_on_none = bool(alert_on_none)                  # bool                  updatable

        self.__aggregation_period = aggregation_period              # RecurringPeriod       updatable
        self.__test_interval = test_interval                        # RecurringPeriod       updatable

        self.__creator_email_address = creator_email_address        # string

        self.__to = to                                              # string                updatable
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

        if self.to < other.to:
            return True

        if self.to > other.to:
            return False

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.topic is None or self.field is None or self.aggregation_period is None or \
                self.creator_email_address is None or self.to is None:
            return False

        if not self.has_trigger():
            return False

        if not self.has_valid_thresholds():
            return False

        # if self.test_interval is not None and not self.test_interval < self.aggregation_period:
        #     return False

        return True


    def has_trigger(self):
        return self.alert_on_none or self.lower_threshold is not None or self.upper_threshold is not None


    def has_valid_thresholds(self):
        if self.lower_threshold is None or self.upper_threshold is None:
            return True

        return self.lower_threshold < self.upper_threshold


    def has_valid_aggregation_period(self):
        return self.aggregation_period is not None and self.aggregation_period.is_valid()


    def may_update(self, other):
        if self.id != other.id or self.topic != other.topic or self.field != other.field or \
                self.creator_email_address != other.creator_email_address:
            return False

        return True


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

    def checkpoint(self):     # TODO: needs an offset if test_interval is used
        return self.aggregation_period.checkpoint()


    def cron(self, minutes_offset):
        return self.aggregation_period.cron(minutes_offset)


    def aws_cron(self, minutes_offset):
        return self.aggregation_period.aws_cron(minutes_offset)
        # return self.test_interval.cron(minutes_offset) if self.test_interval else \
        #     self.aggregation_period.cron(minutes_offset)


    def timedelta(self):
        return self.aggregation_period.timedelta()


    def end_datetime(self, origin: LocalizedDatetime):
        return self.aggregation_period.end_datetime(origin)
        # return self.test_interval.end_datetime(origin) if self.test_interval else \
        #     self.aggregation_period.end_datetime(origin)

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['id'] = self.id

        jdict['topic'] = self.topic
        jdict['field'] = self.field

        jdict['lower-threshold'] = self.lower_threshold
        jdict['upper-threshold'] = self.upper_threshold
        jdict['alert-on-none'] = self.alert_on_none

        jdict['aggregation-period'] = self.aggregation_period.as_json()
        jdict['test-interval'] = None if self.test_interval is None else self.test_interval.as_json()

        jdict['creator-email-address'] = self.creator_email_address

        jdict['to'] = self.to
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
    def to(self):
        return self.__to


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
        return "AlertSpecification:{id:%s, topic:%s, field:%s, lower_threshold:%s, upper_threshold:%s, " \
               "alert_on_none:%s, aggregation_period:%s, test_interval:%s, creator_email_address:%s, " \
               "to:%s, cc_list:%s, suspended:%s}" %  \
               (self.id, self.topic, self.field, self.lower_threshold, self.upper_threshold,
                self.alert_on_none, self.aggregation_period, self.test_interval, self.creator_email_address,
                self.to, self.cc_list, self.suspended)
