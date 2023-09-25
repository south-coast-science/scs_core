"""
Created on 17 Jan 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.security.cognito_user import CognitoUserIdentity
from scs_core.aws.security.organisation import Organisation, OrganisationPathRoot, OrganisationUser, \
    OrganisationUserPath, OrganisationDevice

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class OrganisationManager(APIClient):
    """
    classdocs
    """

    __MANAGER_URL = "https://04h65m94o8.execute-api.us-west-2.amazonaws.com/default/OrganisationManager"
    __EXECUTIVE_URL = "https://19tm2j6odj.execute-api.us-west-2.amazonaws.com/default/OrganisationExecutive"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------
    # Organisation...

    def find_organisations(self, token):
        url = '/'.join((self.__MANAGER_URL, 'organisation'))

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(Organisation.construct_from_jdict(jdict) for jdict in response.json())


    def find_child_organisations(self, token, label):
        url = '/'.join((self.__MANAGER_URL, 'organisation'))
        payload = JSONify.dumps({"ParentLabel": label})

        response = requests.get(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return tuple(Organisation.construct_from_jdict(jdict) for jdict in response.json())


    def get_organisation_by_label(self, token, label):
        url = '/'.join((self.__MANAGER_URL, 'organisation'))
        payload = JSONify.dumps({"Label": label})

        response = requests.get(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return Organisation.construct_from_jdict(response.json())


    def insert_organisation(self, token, organisation):
        url = '/'.join((self.__EXECUTIVE_URL, 'organisation'))
        payload = JSONify.dumps(organisation)

        response = requests.post(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return Organisation.construct_from_jdict(response.json())


    def update_organisation(self, token, organisation):
        url = '/'.join((self.__MANAGER_URL, 'organisation'))
        payload = JSONify.dumps(organisation)

        response = requests.patch(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    def delete_organisation(self, token, org_id):
        url = '/'.join((self.__EXECUTIVE_URL, 'organisation'))
        payload = JSONify.dumps({"OrgID": org_id})

        response = requests.delete(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationPathRoot...

    def find_oprs(self, token, org_id=None):
        url = '/'.join((self.__MANAGER_URL, 'opr'))
        payload = {}

        if org_id:
            payload['OrgID'] = org_id

        response = requests.get(url, headers=self._token_headers(token), data=JSONify.dumps(payload))
        self._check_response(response)

        return tuple(OrganisationPathRoot.construct_from_jdict(jdict) for jdict in response.json())


    def get_opr_by_path_root(self, token, path_root):
        url = '/'.join((self.__MANAGER_URL, 'opr'))
        payload = JSONify.dumps({"PathRoot": path_root})

        response = requests.get(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return OrganisationPathRoot.construct_from_jdict(response.json())


    def insert_opr(self, token, opr):
        url = '/'.join((self.__EXECUTIVE_URL, 'opr'))
        payload = JSONify.dumps(opr)

        response = requests.post(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return OrganisationPathRoot.construct_from_jdict(response.json())


    def delete_opr(self, token, opr_id):
        url = '/'.join((self.__EXECUTIVE_URL, 'opr'))
        payload = JSONify.dumps({"OPRID": opr_id})

        response = requests.delete(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationUser...

    def find_users(self, token):
        url = '/'.join((self.__MANAGER_URL, 'user'))

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(OrganisationUser.construct_from_jdict(jdict) for jdict in response.json())


    def find_users_by_organisation(self, token, org_id):
        url = '/'.join((self.__MANAGER_URL, 'user'))
        payload = JSONify.dumps({"OrgID": org_id})

        response = requests.get(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return tuple(OrganisationUser.construct_from_jdict(jdict) for jdict in response.json())


    def find_cognito_users_by_organisation(self, token, org_id):
        url = '/'.join((self.__MANAGER_URL, 'cognito-user'))
        payload = JSONify.dumps({"OrgID": org_id})

        response = requests.get(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return tuple(CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_users_by_username(self, token, username):
        url = '/'.join((self.__MANAGER_URL, 'user'))
        payload = JSONify.dumps({"Username": username})

        response = requests.get(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return tuple(OrganisationUser.construct_from_jdict(jdict) for jdict in response.json())


    def get_user(self, token, username, org_id):
        url = '/'.join((self.__MANAGER_URL, 'user'))
        payload = JSONify.dumps({"Username": username, "OrgID": org_id})

        response = requests.get(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return OrganisationUser.construct_from_jdict(response.json())


    def assert_user(self, token, user):
        url = '/'.join((self.__MANAGER_URL, 'user'))
        payload = JSONify.dumps(user)

        response = requests.post(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    def delete_user(self, token, username, org_id):
        url = '/'.join((self.__EXECUTIVE_URL, 'user'))
        payload = JSONify.dumps({"Username": username, "OrgID": org_id})

        response = requests.delete(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationUserPath...

    def find_oups(self, token, username=None, opr_id=None):
        url = '/'.join((self.__MANAGER_URL, 'oup'))
        payload = {}

        if username:
            payload['Username'] = username

        if opr_id:
            payload['OPRID'] = opr_id

        response = requests.get(url, headers=self._token_headers(token), data=JSONify.dumps(payload))
        self._check_response(response)

        return tuple(OrganisationUserPath.construct_from_jdict(jdict) for jdict in response.json())


    def assert_oup(self, token, oup):
        url = '/'.join((self.__MANAGER_URL, 'oup'))
        payload = JSONify.dumps(oup)

        response = requests.post(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    def delete_oup(self, token, oup):
        url = '/'.join((self.__MANAGER_URL, 'oup'))
        payload = JSONify.dumps(oup)

        response = requests.delete(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationDevice...

    def find_devices(self, token):
        url = '/'.join((self.__MANAGER_URL, 'device'))

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(OrganisationDevice.construct_from_jdict(jdict) for jdict in response.json())


    def find_devices_by_tag(self, token, device_tag):
        url = '/'.join((self.__MANAGER_URL, 'device'))
        payload = JSONify.dumps({"DeviceTag": device_tag})

        response = requests.get(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return tuple(OrganisationDevice.construct_from_jdict(jdict) for jdict in response.json())


    def find_devices_by_organisation(self, token, org_id):
        url = '/'.join((self.__MANAGER_URL, 'device'))
        payload = JSONify.dumps({"OrgID": org_id})

        response = requests.get(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return tuple(OrganisationDevice.construct_from_jdict(jdict) for jdict in response.json())


    def assert_device(self, token, device):
        url = '/'.join((self.__EXECUTIVE_URL, 'device'))
        payload = JSONify.dumps(device)

        response = requests.post(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    def delete_device(self, token, device_tag):
        url = '/'.join((self.__EXECUTIVE_URL, 'device'))
        payload = JSONify.dumps({"DeviceTag": device_tag})

        response = requests.delete(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


# --------------------------------------------------------------------------------------------------------------------

class DeviceOrganisationManager(APIClient):
    """
    classdocs
    """

    __MANAGER_URL = "https://6fs21ckyci.execute-api.us-west-2.amazonaws.com/default/DeviceOrganisationManager"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationDevice...

    def location_path_in_use(self, token, location_path):
        payload = JSONify.dumps({"LocationPath": location_path})

        response = requests.get(self.__MANAGER_URL, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return json.loads(response.json())
