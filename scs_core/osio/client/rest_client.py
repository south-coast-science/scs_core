'''
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

org-id: south-coast-science-dev
API KEY: 43308b72-ad41-4555-b075-b4245c1971db
New device password:QMicOCZw


CURLOPT_HTTPHEADER => array('Accept: application/json', 'Authorization: api-key ' . AOC_OPENSENSORS_API_KEY),
'''

import json

from collections import OrderedDict

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class RESTClient(object):
    '''
    classdocs
    '''

    __HOST = "api.opensensors.io"

    __HEADER_ACCEPT = "application/json"
    __HEADER_AUTHORIZATION = "api-key "


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, api_key):
        '''
        Constructor
        '''
        self.__http_client = http_client
        self.__api_key = api_key


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        self.__http_client.connect(RESTClient.__HOST)


    def close(self):
        self.__http_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def get(self, path, params = None):
        response_jstr = self.__http_client.get(path, params, self.__headers)
        response_jdict = json.loads(response_jstr, object_pairs_hook=OrderedDict)

        return response_jdict


    def post(self, path, payload_jdict):                # TODO: make the jdict here?
        payload_jstr = JSONify.dumps(payload_jdict)

        response_jstr = self.__http_client.post(path, payload_jstr, self.__headers)
        response_jdict = json.loads(response_jstr, object_pairs_hook=OrderedDict)

        return response_jdict


    def put(self, path, payload_jdict):                # TODO: make the jdict here?
        payload_jstr = JSONify.dumps(payload_jdict)

        response_jstr = self.__http_client.put(path, payload_jstr, self.__headers)
        response_jdict = json.loads(response_jstr, object_pairs_hook=OrderedDict)

        return response_jdict


    def delete(self, path):
        response_jstr = self.__http_client.delete(path, self.__headers)
        response_jdict = json.loads(response_jstr, object_pairs_hook=OrderedDict)

        return response_jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def __headers(self):
        return {"Accept": RESTClient.__HEADER_ACCEPT, "Authorization": RESTClient.__HEADER_AUTHORIZATION + self.__api_key}


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
            return "RESTClient:{http_client:%s, api_key:%s}" % (self.__http_client, self.__api_key)
