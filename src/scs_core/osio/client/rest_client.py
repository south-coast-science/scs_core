"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

header:
CURLOPT_HTTPHEADER => array('Accept: application/json', 'Authorization: api-key ' . AOC_OPENSENSORS_API_KEY),
"""

import json

from scs_core.data.json import JSONify

from scs_core.osio.client.client_exception import ClientException

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.http_status import HTTPStatus


# --------------------------------------------------------------------------------------------------------------------

class RESTClient(object):
    """
    classdocs
    """

    __HOST = "api.opensensors.io"               # hard-coded URL

    __VERIFIED = False                          # False - ignore invalid SSL certificates

    __HEADER_ACCEPT = "application/json"
    __HEADER_AUTHORIZATION = "api-key "


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, api_key):
        """
        Constructor
        """
        self.__http_client = http_client
        self.__api_key = api_key


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self, timeout=None):
        self.__http_client.connect(self.__HOST, verified=self.__VERIFIED, timeout=timeout)


    def close(self):
        self.__http_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def get(self, path, params=None):
        try:
            response_jstr = self.__http_client.get(path, params, self.__headers)
        except HTTPException as ex:
            if ex.status == HTTPStatus.NOT_FOUND:
                return None
            else:
                raise ClientException.construct(ex) from ex

        try:
            response = json.loads(response_jstr)
        except ValueError:
            response = None

        return response


    def post(self, path, payload_jdict):                # TODO: make the jdict here?
        payload_jstr = JSONify.dumps(payload_jdict)

        # print("RESTClient.post: path: %s payload: %s" % (path, payload_jstr))

        try:
            response_jstr = self.__http_client.post(path, payload_jstr, self.__headers)
        except HTTPException as ex:
            raise ClientException.construct(ex) from ex

        try:
            response = json.loads(response_jstr)
        except ValueError:
            response = None

        return response


    def put(self, path, payload_jdict):                # TODO: make the jdict here?
        payload_jstr = JSONify.dumps(payload_jdict)

        # print("RESTClient.put: path: %s payload: %s" % (path, payload_jstr))

        try:
            response_jstr = self.__http_client.put(path, payload_jstr, self.__headers)
        except HTTPException as ex:
            raise ClientException.construct(ex) from ex

        try:
            response = json.loads(response_jstr)
        except ValueError:
            response = None

        return response


    def delete(self, path):
        try:
            response_jstr = self.__http_client.delete(path, self.__headers)
        except HTTPException as ex:
            raise ClientException.construct(ex) from ex

        try:
            response = json.loads(response_jstr)
        except ValueError:
            response = None

        return response


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def __headers(self):
        return {"Accept": self.__HEADER_ACCEPT,
                "Authorization": self.__HEADER_AUTHORIZATION + self.__api_key}


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "RESTClient:{http_client:%s, api_key:%s}" % (self.__http_client, self.__api_key)
