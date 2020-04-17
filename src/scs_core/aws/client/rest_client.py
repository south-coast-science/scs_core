"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://xy1eszuu23.execute-api.us-west-2.amazonaws.com/staging/topicMessages?
topic=south-coast-science-dev/production-test/loc/1/gases&
startTime=2018-03-31T07:50:59.712Z&
endTime=2018-03-31T07:55:59.712Z

header:
CURLOPT_HTTPHEADER => array('Accept: application/json', 'Authorization: api-key ' . AWS_API_KEY),
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONify

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.http_status import HTTPStatus


# --------------------------------------------------------------------------------------------------------------------

class RESTClient(object):
    """
    classdocs
    """

    __HEADER_ACCEPT = "application/json"
    __HEADER_AUTHORIZATION = "api-key "


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, auth):
        """
        Constructor
        """
        self.__http_client = http_client
        self.__auth = auth


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        self.__http_client.connect(self.__auth.endpoint, timeout=60)


    def close(self):
        self.__http_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def get(self, path, params=None):
        # print("RESTClient.get: path: %s params: %s" % (path, params))

        try:
            response_jstr = self.__http_client.get(path, params, self.__headers)
        except HTTPException as exc:
            if exc.status == HTTPStatus.NOT_FOUND:
                return None

            else:
                raise exc

        try:
            response = json.loads(response_jstr, object_hook=OrderedDict)
        except ValueError:
            response = None

        return response


    def post(self, path, payload_jdict):
        payload_jstr = JSONify.dumps(payload_jdict)

        # print("RESTClient.post: path: %s payload: %s" % (path, payload_jstr))

        response_jstr = self.__http_client.post(path, payload_jstr, self.__headers)

        try:
            response = json.loads(response_jstr, object_hook=OrderedDict)
        except ValueError:
            response = None

        return response


    def put(self, path, payload_jdict):
        payload_jstr = JSONify.dumps(payload_jdict)

        # print("RESTClient.put: path: %s payload: %s" % (path, payload_jstr))

        response_jstr = self.__http_client.put(path, payload_jstr, self.__headers)

        try:
            response = json.loads(response_jstr, object_hook=OrderedDict)
        except ValueError:
            response = None

        return response


    def delete(self, path):
        response_jstr = self.__http_client.delete(path, self.__headers)

        try:
            response = json.loads(response_jstr, object_hook=OrderedDict)
        except ValueError:
            response = None

        return response


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def __headers(self):
        return {"Accept": RESTClient.__HEADER_ACCEPT,
                "Authorization": RESTClient.__HEADER_AUTHORIZATION + self.__auth.api_key}


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "RESTClient:{http_client:%s, auth:%s}" % (self.__http_client, self.__auth)
