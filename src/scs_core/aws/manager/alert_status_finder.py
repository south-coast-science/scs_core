"""
Created on 17 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from enum import Enum
from http import HTTPStatus

from scs_core.aws.data.alert import AlertStatus
from scs_core.aws.data.http_response import HTTPResponse

from scs_core.data.datum import Datum
from scs_core.data.str import Str

from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

class AlertStatusFinder(object):
    """
    classdocs
    """

    __URL = ""

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, auth):
        self.__http_client = http_client
        self.__auth = auth


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, topic_filter, path_filter, id_filter, cause_filter, response_mode):
        request = AlertStatusRequest(topic_filter, path_filter, id_filter, cause_filter, response_mode)
        headers = {'Authorization': self.__auth.email_address}

        response = self.__http_client.get(self.__URL, headers=headers, params=request.params())

        return AlertStatusResponse.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AlertStatusFinder:{auth:%s}" % self.__auth


# --------------------------------------------------------------------------------------------------------------------

class AlertStatusRequest(object):
    """
    classdocs
    """

    MODE = Enum('Mode', 'HISTORY LATEST')

    TOPIC_FILTER = 'tag'
    PATH_FILTER = 'path'
    ID_FILTER = 'id'
    CAUSE_FILTER = 'cause'
    RESPONSE_MODE = 'responseMode'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        topic_filter = qsp.get(cls.TOPIC_FILTER)
        path_filter = qsp.get(cls.PATH_FILTER)
        id_filter = qsp.get(cls.ID_FILTER)
        cause_filter = qsp.get(cls.CAUSE_FILTER)

        try:
            response_mode = cls.MODE[qsp.get(cls.RESPONSE_MODE)]
        except KeyError:
            response_mode = None

        return cls(topic_filter, path_filter, id_filter, cause_filter, response_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic_filter, path_filter, id_filter, cause_filter, response_mode):
        """
        Constructor
        """
        self.__topic_filter = topic_filter                          # string
        self.__path_filter = path_filter                            # string
        self.__id_filter = Datum.int(id_filter)                     # int
        self.__cause_filter = cause_filter                          # string
        self.__response_mode = response_mode                        # enum


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.response_mode is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            self.TOPIC_FILTER: self.topic_filter,
            self.PATH_FILTER: self.path_filter,
            self.ID_FILTER: self.id_filter,
            self.CAUSE_FILTER: self.cause_filter,
            self.RESPONSE_MODE: self.response_mode.name
        }

        return params


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic_filter(self):
        return self.__topic_filter


    @property
    def path_filter(self):
        return self.__path_filter


    @property
    def id_filter(self):
        return self.__id_filter


    @property
    def cause_filter(self):
        return self.__cause_filter


    @property
    def response_mode(self):
        return self.__response_mode


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AlertStatusRequest:{topic_filter:%s, path_filter:%s, id_filter:%s, cause_filter:%s, " \
               "response_mode:%s}" % \
               (self.topic_filter, self.path_filter, self.id_filter, self.cause_filter,
                self.response_mode)


# --------------------------------------------------------------------------------------------------------------------

class AlertStatusResponse(HTTPResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # print("jdict: %s" % jdict)

        status = HTTPStatus(jdict.get('statusCode'))

        if status != HTTPStatus.OK:
            raise HTTPException(status.value, status.phrase, status.description)

        mode = AlertStatusRequest.MODE[jdict.get('mode')]

        alert_statuses = []
        if jdict.get('Items'):
            for alert_jdict in jdict.get('Items'):
                alert_statuses.append(AlertStatus.construct_from_jdict(alert_jdict))

        next_url = jdict.get('next')

        return cls(status, mode, alert_statuses, next_url=next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, mode, alert_statuses, next_url=None):
        """
        Constructor
        """
        super().__init__(status)

        self.__mode = mode                              # AlertStatusRequest.Mode member
        self.__alert_statuses = alert_statuses          # array of AlertStatus
        self.__next_url = next_url                      # URL string


    def __len__(self):
        return len(self.alert_statuses)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['statusCode'] = self.status.value

        if self.mode is not None:
            jdict['mode'] = self.mode.name

        if self.alert_statuses is not None:
            jdict['alert-statuses'] = self.alert_statuses

        if self.next_url is not None:
            jdict['next'] = self.next_url

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mode(self):
        return self.__mode


    @property
    def alert_statuses(self):
        return self.__alert_statuses


    @property
    def next_url(self):
        return self.__next_url


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AlertStatusResponse:{status:%s, mode:%s, alert_statuses:%s, next_url:%s}" % \
               (self.status, self.mode, Str.collection(self.alert_statuses), self.next_url)
