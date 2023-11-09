"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import ssl

import http.client

import urllib.parse

from socket import gaierror, timeout as timeout_error

from scs_core.client.http_exception import HTTPException
from scs_core.client.http_status import HTTPStatus
from scs_core.client.resource_unavailable_exception import ResourceUnavailableException


# --------------------------------------------------------------------------------------------------------------------

class HTTPClient(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__conn = None
        self.__host = None


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self, host, secure=True, verified=True, timeout=None):
        # print("connect: host: {}, timeout: {}".format(host, timeout), file=sys.stderr)

        self.__host = host

        if secure:
            # noinspection PyProtectedMember,PyUnresolvedReferences
            context = None if verified else ssl._create_unverified_context()

            if timeout is not None:
                self.__conn = http.client.HTTPSConnection(host, context=context, timeout=timeout)
            else:
                self.__conn = http.client.HTTPSConnection(host, context=context)

        else:
            if timeout is not None:
                self.__conn = http.client.HTTPConnection(host, timeout=timeout)
            else:
                self.__conn = http.client.HTTPConnection(host)


    def close(self):
        if self.__conn:
            self.__conn.close()


    # ----------------------------------------------------------------------------------------------------------------

    def get(self, path, payload, headers):
        # data...
        params = urllib.parse.urlencode(payload) if payload else None
        query = path + '?' + params if params else path

        # print("get: query: {}".format(query))
        # print("headers: %s " % headers)

        # request...
        response = self.__request("GET", query, None, headers)
        data = response.read()

        # error...
        if response.status != HTTPStatus.OK:
            raise HTTPException.construct_from_res(response, data)

        # print("response: %s " % data.decode())

        return data.decode()


    def post(self, path, payload, headers):
        # request...
        response = self.__request("POST", path, payload, headers)
        data = response.read()

        # error...
        if response.status != HTTPStatus.OK and response.status != HTTPStatus.CREATED:
            raise HTTPException.construct_from_res(response, data)

        return data.decode()


    def put(self, path, payload, headers):
        # request...
        response = self.__request("PUT", path, payload, headers)
        data = response.read()

        # error...
        if response.status != HTTPStatus.OK and response.status != HTTPStatus.NO_CONTENT:
            raise HTTPException.construct_from_res(response, data)

        return data.decode()


    def delete(self, path, headers):
        # request...
        response = self.__request("DELETE", path, "", headers)
        data = response.read()

        # error...
        if response.status != HTTPStatus.OK and response.status != HTTPStatus.NO_CONTENT:
            raise HTTPException.construct_from_res(response, data)

        return data.decode()


    # ----------------------------------------------------------------------------------------------------------------

    def __request(self, method, url, body, headers):
        try:
            self.__conn.request(method, url, body=body, headers=headers)
            return self.__conn.getresponse()

        except (gaierror, timeout_error, http.client.CannotSendRequest, OSError) as ex:
            self.__conn.close()

            raise ResourceUnavailableException(self.__host + url, ex)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HTTPClient:{conn:%s, host:%s}" % (self.__conn, self.__host)
