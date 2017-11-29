"""
Created on 8 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import urllib.parse

from scs_core.osio.client.rest_client import RESTClient
from scs_core.osio.data.organisation import Organisation


# --------------------------------------------------------------------------------------------------------------------

class OrganisationManager(object):
    """
    classdocs
    """
    __FINDER_BATCH_SIZE = 100

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, api_key):
        """
        Constructor
        """
        self.__rest_client = RESTClient(http_client, api_key)


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, org_id):
        request_path = '/v1/orgs/' + urllib.parse.quote(org_id, '')

        # request...
        self.__rest_client.connect()

        try:
            response_jdict = self.__rest_client.get(request_path)
        except RuntimeError:
            response_jdict = None

        self.__rest_client.close()

        topic = Organisation.construct_from_jdict(response_jdict)

        return topic


    def find_owned_by_user(self, org_id):
        orgs = []

        # request...
        self.__rest_client.connect()

        try:
            for batch in self.__get(org_id):
                orgs.extend(batch)

        finally:
            self.__rest_client.close()

        return orgs


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, org):
        request_path = '/v1/orgs'

        # request...
        self.__rest_client.connect()

        try:
            response = self.__rest_client.post(request_path, org.as_json())

        finally:
            self.__rest_client.close()

        print("create response: %s" % response)

        return response


    def update(self, org_id, org):
        request_path = '/v1/orgs/' + org_id

        # request...
        self.__rest_client.connect()

        try:
            self.__rest_client.put(request_path, org.as_json())
        finally:
            self.__rest_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __get(self, user_id):
        request_path = '/v12/users/' + user_id + '/owned-orgs'
        params = {'offset': 0, 'count': self.__FINDER_BATCH_SIZE}

        while True:
            # request...
            response_jdict = self.__rest_client.get(request_path, params)

            # organisations...
            orgs = [Organisation.construct_from_jdict(org_jdict) for org_jdict in response_jdict] \
                if response_jdict else []

            yield orgs

            if len(orgs) == 0:
                break

            # next...
            params['offset'] += len(orgs)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OrganisationManager:{rest_client:%s}" % self.__rest_client
