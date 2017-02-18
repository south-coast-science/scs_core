"""
Created on 13 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

api auth:
{"org-id": "south-coast-science-dev", "api-key": "43308b72-ad41-4555-b075-b4245c1971db"}

device auth:
{"username": "southcoastscience-dev", "device-id": "5406", "device-password": "jtxSrK2e"}
"""

import urllib.parse

from scs_core.osio.client.rest_client import RESTClient
from scs_core.osio.data.device import Device


# TODO: device_id should be client_id

# --------------------------------------------------------------------------------------------------------------------

class DeviceManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, api_key):
        """
        Constructor
        """
        self.__rest_client = RESTClient(http_client, api_key)


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_user(self, user_id, device_id):
        path = '/v1/users/' + user_id + '/devices/' + str(device_id)

        # request...
        self.__rest_client.connect()

        try:
            response_jdict = self.__rest_client.get(path)
        except RuntimeError:
            response_jdict = None

        self.__rest_client.close()

        device = Device.construct_from_jdict(response_jdict)

        return device


    def find_for_org(self, org_id, device_id):
        path = '/v1/orgs/' + org_id + '/devices/' + str(device_id)

        # request...
        self.__rest_client.connect()

        try:
            response_jdict = self.__rest_client.get(path)
        except RuntimeError:
            response_jdict = None

        self.__rest_client.close()

        device = Device.construct_from_jdict(response_jdict)

        return device


    def find_all_for_user(self, user_id):
        path = '/v1/users/southcoastscience-dev/devices'

        # request...
        self.__rest_client.connect()

        response_jdict = self.__rest_client.get(path, {'user-id': user_id})

        self.__rest_client.close()

        devices = [Device.construct_from_jdict(device_jdict) for device_jdict in response_jdict] if response_jdict else []

        return devices


    def find_all_for_org(self, org_id):
        path = '/v1/orgs/' + org_id + '/devices'

        # request...
        self.__rest_client.connect()

        response_jdict = self.__rest_client.get(path)

        self.__rest_client.close()

        devices = [Device.construct_from_jdict(device_jdict) for device_jdict in response_jdict] if response_jdict else []

        return devices


    def create(self, user_id, device):
        path = '/v1/users/' + user_id + '/devices'

        # request...
        self.__rest_client.connect()

        response = self.__rest_client.post(path, device.as_json())

        self.__rest_client.close()

        # TODO: returns something?


    def update(self):
        pass


    def delete(self, device_id):
        path = '/v1/topics/' + urllib.parse.quote(topic_path, '')

        # request...
        self.__rest_client.connect()

        response = self.__rest_client.delete(path)

        self.__rest_client.close()

        success = response == ''

        return success


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceManager:{rest_client:%s}" % self.__rest_client
