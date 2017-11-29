"""
Created on 13 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

"""

from scs_core.osio.client.rest_client import RESTClient
from scs_core.osio.data.device import Device
from scs_core.osio.data.device_summary import DeviceSummary


# --------------------------------------------------------------------------------------------------------------------

class DeviceManager(object):
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

    def find(self, org_id, client_id):
        request_path = '/v1/orgs/' + org_id + '/devices/' + client_id

        # request...
        self.__rest_client.connect()

        try:
            response_jdict = self.__rest_client.get(request_path)
        except RuntimeError:
            response_jdict = None

        self.__rest_client.close()

        device = Device.construct_from_jdict(response_jdict)

        return device


    def find_for_name(self, org_id, name):
        devices = self.find_all_for_org(org_id)

        for device in devices:                              # warning: unique only by convention
            if device.name == name:
                return self.find(org_id, device.client_id)

        return None


    def find_all_for_user(self, user_id):
        request_path = '/v1/users/' + user_id + '/devices'
        devices = []

        # request...
        self.__rest_client.connect()

        try:
            for batch in self.__find(request_path, {'user-id': user_id}):
                devices.extend(batch)

        finally:
            self.__rest_client.close()

        return devices


    def find_all_for_org(self, org_id):
        request_path = '/v1/orgs/' + org_id + '/devices'
        devices = []

        # request...
        self.__rest_client.connect()

        try:
            for batch in self.__find(request_path):
                devices.extend(batch)

        finally:
            self.__rest_client.close()

        return devices


    # ----------------------------------------------------------------------------------------------------------------

    def __find(self, request_path, params=None):
        if params is None:
            params = {}

        params['offset'] = 0
        params['count'] = self.__FINDER_BATCH_SIZE

        while True:
            # request...
            response_jdict = self.__rest_client.get(request_path, params)

            devices = [DeviceSummary.construct_from_jdict(jdict) for jdict in response_jdict] if response_jdict else []

            yield devices

            if len(devices) == 0:
                break

            # next...
            params['offset'] += len(devices)


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, user_id, device):
        request_path = '/v1/users/' + user_id + '/devices'

        # request...
        self.__rest_client.connect()

        try:
            response_jdict = self.__rest_client.post(request_path, device.as_json())
        finally:
            self.__rest_client.close()

        device = Device.construct_from_jdict(response_jdict)

        return device


    def update(self, org_id, system_id, device):
        request_path = '/v1/orgs/' + org_id + '/devices/' + system_id

        # request...
        self.__rest_client.connect()

        try:
            self.__rest_client.put(request_path, device.as_json())
        finally:
            self.__rest_client.close()


    def delete(self, user_id, client_id):
        request_path = '/v1/users/' + user_id + '/devices/' + client_id

        # request...
        self.__rest_client.connect()

        try:
            self.__rest_client.delete(request_path)
        finally:
            self.__rest_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceManager:{rest_client:%s}" % self.__rest_client
