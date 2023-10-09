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

from scs_core.data.json import JSONify

from scs_core.client.http_client import HTTPClient
from scs_core.client.http_exception import HTTPException
from scs_core.client.http_status import HTTPStatus


# --------------------------------------------------------------------------------------------------------------------

class RESTClient(object):
    """
    classdocs
    """

    __HOST = "aws.southcoastscience.com"

    __HEADER_ACCEPT = "application/json"
    __HEADER_AUTHORIZATION = "api-key"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, api_key=None):
        """
        Constructor
        """
        self.__http_client = HTTPClient()
        self.__api_key = api_key


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        self.__http_client.connect(self.__HOST)


    def close(self):
        self.__http_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def get(self, path, params=None):
        print("RESTClient.get: path: %s params: %s headers:%s" % (path, params, self.__headers))

        try:
            response_jstr = self.__http_client.get(path, params, self.__headers)
            # print("response_jstr: %s" % response_jstr, file=sys.stderr)
            # print("-", file=sys.stderr)

        except HTTPException as ex:
            # print("exc: %s" % exc, file=sys.stderr)
            # print("-", file=sys.stderr)

            if ex.status == HTTPStatus.NOT_FOUND:
                return None

            else:
                raise ex

        try:
            response = json.loads(response_jstr)
        except ValueError:
            response = None

        return response


    def post(self, path, payload_jdict):
        payload_jstr = JSONify.dumps(payload_jdict)

        # print("RESTClient.post: path: %s payload: %s" % (path, payload_jstr))

        response_jstr = self.__http_client.post(path, payload_jstr, self.__headers)

        try:
            response = json.loads(response_jstr)
        except ValueError:
            response = None

        return response


    def put(self, path, payload_jdict):
        payload_jstr = JSONify.dumps(payload_jdict)

        # print("RESTClient.put: path: %s payload: %s" % (path, payload_jstr))

        response_jstr = self.__http_client.put(path, payload_jstr, self.__headers)

        try:
            response = json.loads(response_jstr)
        except ValueError:
            response = None

        return response


    def delete(self, path):
        response_jstr = self.__http_client.delete(path, self.__headers)

        try:
            response = json.loads(response_jstr)
        except ValueError:
            response = None

        return response


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def __headers(self):
        headers = {
            "Accept": self.__HEADER_ACCEPT,
        }

        if self.__api_key is not None:
            headers["Authorization"] = ' '.join((self.__HEADER_AUTHORIZATION, self.__api_key))

        return headers


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "RESTClient:{host:%s, api_key:%s}" % (self.__HOST, self.__api_key)
