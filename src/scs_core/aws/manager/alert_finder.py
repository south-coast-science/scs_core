"""
Created on 17 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from http import HTTPStatus

from scs_core.aws.data.alert import Alert
from scs_core.aws.data.http_response import HTTPResponse

from scs_core.data.datum import Datum
from scs_core.data.str import Str

from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

class AlertFinder(object):
    """
    classdocs
    """

    __URL = ""

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, auth):
        self.__http_client = http_client
        self.__auth = auth


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, topic_filter, path_filter, id_filter, creator_filter):
        request = AlertFinderRequest(topic_filter, path_filter, id_filter, creator_filter)
        headers = {'Authorization': self.__auth.email_address}

        response = self.__http_client.get(self.__URL, headers=headers, params=request.params())

        return AlertFinderResponse.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AlertFinder:{auth:%s}" % self.__auth


# --------------------------------------------------------------------------------------------------------------------

class AlertFinderRequest(object):
    """
    classdocs
    """

    ID_FILTER = 'id'
    TOPIC_FILTER = 'tag'
    PATH_FILTER = 'path'
    CREATOR_FILTER = 'creator'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        id_filter = qsp.get(cls.ID_FILTER)
        topic_filter = qsp.get(cls.TOPIC_FILTER)
        path_filter = qsp.get(cls.PATH_FILTER)
        creator_filter = qsp.get(cls.CREATOR_FILTER)

        return cls(id_filter, topic_filter, path_filter, creator_filter)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id_filter, topic_filter, path_filter, creator_filter):
        """
        Constructor
        """
        self.__id_filter = Datum.int(id_filter)                     # int
        self.__topic_filter = topic_filter                          # string
        self.__path_filter = path_filter                            # string
        self.__creator_filter = creator_filter                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.id_filter is None and self.topic_filter is None and self.path_filter is None and \
                self.creator_filter is None:
            return False

        if self.id_filter is not None and (self.topic_filter is not None or self.path_filter is not None):
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            self.ID_FILTER: self.id_filter,
            self.TOPIC_FILTER: self.topic_filter,
            self.PATH_FILTER: self.path_filter,
            self.CREATOR_FILTER: self.creator_filter
        }

        return params


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id_filter(self):
        return self.__id_filter


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
        return "AlertFinderRequest:{id_filter:%s, topic_filter:%s, path_filter:%s, creator_filter:%s}" % \
               (self.id_filter, self.topic_filter, self.path_filter, self.creator_filter)


# --------------------------------------------------------------------------------------------------------------------

class AlertFinderResponse(HTTPResponse):
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

        alerts = []
        if jdict.get('Items'):
            for alert_jdict in jdict.get('Items'):
                alerts.append(Alert.construct_from_jdict(alert_jdict))

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
            jdict['alerts'] = self.alerts

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
        return "AlertFinderResponse:{status:%s, alerts:%s, next_url:%s}" % \
               (self.status, Str.collection(self.alerts), self.next_url)
