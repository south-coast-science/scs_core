"""
Created on 30 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class HTTPException(RuntimeError, JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_res(cls, response, encoded_data):
        status = None if response.status is None else int(response.status)
        reason = response.reason
        data = encoded_data.decode()

        return cls.construct(status, reason, data)


    @classmethod
    def construct(cls, status, reason, data):
        if status == HTTPBadRequestException.STATUS:
            return HTTPBadRequestException(status, reason, data)

        if status == HTTPUnauthorizedException.STATUS:
            return HTTPUnauthorizedException(status, reason, data)

        if status == HTTPNotFoundException.STATUS:
            return HTTPNotFoundException(status, reason, data)

        if status == HTTPNotAllowedException.STATUS:
            return HTTPNotAllowedException(status, reason, data)

        if status == HTTPConflictException.STATUS:
            return HTTPConflictException(status, reason, data)

        if status == HTTPGoneException.STATUS:
            return HTTPGoneException(status, reason, data)

        if status == HTTPBadGatewayException.STATUS:
            return HTTPBadGatewayException(status, reason, data)

        if status == HTTPServiceUnavailableException.STATUS:
            return HTTPServiceUnavailableException(status, reason, data)

        if status == HTTPGatewayTimeoutException.STATUS:
            return HTTPGatewayTimeoutException(status, reason, data)

        return cls(status, reason, data)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason, data):
        """
        Constructor
        """
        self.__status = status              # int
        self.__reason = reason              # string
        self.__data = data                  # string (may be JSON)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['status'] = self.status
        jdict['reason'] = self.reason
        jdict['data'] = self.data

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def status(self):
        return self.__status


    @property
    def reason(self):
        return self.__reason


    @property
    def data(self):
        return self.__data


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def error_report(self):
        now = LocalizedDatetime.now().utc().as_iso8601()

        if self.data is None:
            return "%s: HTTP response: %s (%s)" % (now, self.status, self.reason)

        return "%s: HTTP response: %s (%s) %s" % (now, self.status, self.reason, self.data)



    def __str__(self, *args, **kwargs):
        name = self.__class__.__name__

        return name + ":{status:%s, reason:%s, data:%s}" % (self.status, self.reason, self.data)


# --------------------------------------------------------------------------------------------------------------------
# 400 client errors...

class HTTPBadRequestException(HTTPException):
    """
    classdocs
    """
    STATUS = 400

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason, data):
        super().__init__(status, reason, data)


# --------------------------------------------------------------------------------------------------------------------

class HTTPUnauthorizedException(HTTPException):
    """
    classdocs
    """
    STATUS = 401

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason, data):
        super().__init__(status, reason, data)


# --------------------------------------------------------------------------------------------------------------------

class HTTPNotFoundException(HTTPException):
    """
    classdocs
    """
    STATUS = 404

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason, data):
        super().__init__(status, reason, data)


# --------------------------------------------------------------------------------------------------------------------

class HTTPNotAllowedException(HTTPException):
    """
    classdocs
    """
    STATUS = 405

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason, data):
        super().__init__(status, reason, data)


# --------------------------------------------------------------------------------------------------------------------

class HTTPConflictException(HTTPException):
    """
    classdocs
    """
    STATUS = 409

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason, data):
        super().__init__(status, reason, data)


# --------------------------------------------------------------------------------------------------------------------

class HTTPGoneException(HTTPException):
    """
    classdocs
    """
    STATUS = 410

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason, data):
        super().__init__(status, reason, data)


# --------------------------------------------------------------------------------------------------------------------
# 500 server errors...

class HTTPBadGatewayException(HTTPException):
    """
    classdocs
    """
    STATUS = 502

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason, data):
        super().__init__(status, reason, data)


# --------------------------------------------------------------------------------------------------------------------

class HTTPServiceUnavailableException(HTTPException):
    """
    classdocs
    """
    STATUS = 503

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason, data):
        super().__init__(status, reason, data)


# --------------------------------------------------------------------------------------------------------------------

class HTTPGatewayTimeoutException(HTTPException):
    """
    classdocs
    """
    STATUS = 504

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason, data):
        super().__init__(status, reason, data)
