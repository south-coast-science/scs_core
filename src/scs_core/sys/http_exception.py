"""
Created on 30 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class HTTPException(RuntimeError, JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_response(cls, response, encoded_data):
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

        if status == HTTPConflictException.STATUS:
            return HTTPConflictException(status, reason, data)

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

    def __str__(self, *args, **kwargs):
        name = self.__class__.__name__

        return name + ":{status:%s, reason:%s, data:%s}" % (self.status, self.reason, self.data)


# --------------------------------------------------------------------------------------------------------------------

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

class HTTPConflictException(HTTPException):
    """
    classdocs
    """
    STATUS = 409

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason, data):
        super().__init__(status, reason, data)
