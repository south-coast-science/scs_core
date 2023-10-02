"""
Created on 2 Oct 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from http import HTTPStatus

from scs_core.aws.data.http_response import HTTPResponse
from scs_core.aws.monitor.alert.alert import AlertSpecification

from scs_core.client.http_exception import HTTPException

from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class AlertSpecificationFindRequest(object):
    """
    classdocs
    """

    DESCRIPTION_FILTER = 'description'
    TOPIC_FILTER = 'topic'
    PATH_FILTER = 'path'
    CREATOR_FILTER = 'creator'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        description_filter = qsp.get(cls.DESCRIPTION_FILTER)
        topic_filter = qsp.get(cls.TOPIC_FILTER)
        path_filter = qsp.get(cls.PATH_FILTER)
        creator_filter = qsp.get(cls.CREATOR_FILTER)

        return cls(description_filter, topic_filter, path_filter, creator_filter)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, description_filter, topic_filter, path_filter, creator_filter):
        """
        Constructor
        """
        self.__description_filter = description_filter              # string
        self.__topic_filter = topic_filter                          # string
        self.__path_filter = path_filter                            # string
        self.__creator_filter = creator_filter                      # string


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid(cls):
        return True


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        description_filter = self.description_filter if self.description_filter else None

        params = {
            self.DESCRIPTION_FILTER: description_filter,
            self.TOPIC_FILTER: self.topic_filter,
            self.PATH_FILTER: self.path_filter,
            self.CREATOR_FILTER: self.creator_filter
        }

        return params


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def description_filter(self):
        return self.__description_filter


    @property
    def topic_filter(self):
        return self.__topic_filter


    @property
    def path_filter(self):
        return self.__path_filter


    @property
    def creator_filter(self):
        return self.__creator_filter


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AlertSpecificationFindRequest:{description_filter:%s, topic_filter:%s, path_filter:%s, " \
               "creator_filter:%s}" % \
               (self.description_filter, self.topic_filter, self.path_filter,
                self.creator_filter)


# --------------------------------------------------------------------------------------------------------------------

class AlertSpecificationFindResponse(HTTPResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        status = HTTPStatus(jdict.get('statusCode'))

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, status.phrase, status.description)

        alerts = []
        if jdict.get('Items'):
            for alert_jdict in jdict.get('Items'):
                alerts.append(AlertSpecification.construct_from_jdict(alert_jdict))

        next_url = jdict.get('next')

        return cls(status, alerts, next_url=next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, alerts, next_url=None):
        """
        Constructor
        """
        super().__init__(status)

        self.__alerts = alerts                  # array of Alert
        self.__next_url = next_url              # URL string


    def __len__(self):
        return len(self.alerts)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['statusCode'] = self.status.value

        if self.alerts is not None:
            jdict['Items'] = self.alerts

        if self.next_url is not None:
            jdict['next'] = self.next_url

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def alerts(self):
        return self.__alerts


    @property
    def next_url(self):
        return self.__next_url


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AlertSpecificationFindResponse:{status:%s, alerts:%s, next_url:%s}" % \
               (self.status, Str.collection(self.alerts), self.next_url)
