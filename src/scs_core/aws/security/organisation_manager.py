"""
Created on 17 Jan 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint
from scs_core.aws.security.cognito_user import CognitoUserIdentity

from scs_core.aws.security.organisation import Organisation, OrganisationPathRoot, OrganisationUser, \
    OrganisationUserPath, OrganisationDevice

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class DevEndpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('OrgDevAPI/DeviceOrganisationManager',
                   'https://6fs21ckyci.execute-api.us-west-2.amazonaws.com/default/DeviceOrganisationManager')


# --------------------------------------------------------------------------------------------------------------------

class ExecEndpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('OrgExecAPI/OrganisationExecutive',
                   'https://19tm2j6odj.execute-api.us-west-2.amazonaws.com/default/OrganisationExecutive')


# --------------------------------------------------------------------------------------------------------------------

class MgrEndpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('OrgMgrAPI/OrganisationManager',
                   'https://04h65m94o8.execute-api.us-west-2.amazonaws.com/default/OrganisationManager')


# --------------------------------------------------------------------------------------------------------------------

class OrganisationManager(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------
    # Organisation...

    def find_organisations(self, token):
        url = MgrEndpoint.url('organisation')

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(Organisation.construct_from_jdict(jdict) for jdict in response.json())


    def find_child_organisations(self, token, label):
        url = MgrEndpoint.url('organisation')
        params = {"ParentLabel": label}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return tuple(Organisation.construct_from_jdict(jdict) for jdict in response.json())


    def get_organisation(self, token, id):
        url = MgrEndpoint.url('organisation')
        params = {"ID": id}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return Organisation.construct_from_jdict(response.json())


    def get_organisation_by_label(self, token, label):
        url = MgrEndpoint.url('organisation')
        params = {"Label": label}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return Organisation.construct_from_jdict(response.json())


    def insert_organisation(self, token, organisation):
        url = ExecEndpoint.url('organisation')
        payload = JSONify.dumps(organisation)

        response = requests.post(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return Organisation.construct_from_jdict(response.json())


    def update_organisation(self, token, organisation):
        url = MgrEndpoint.url('organisation')
        payload = JSONify.dumps(organisation)

        response = requests.patch(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    def delete_organisation(self, token, org_id):
        url = ExecEndpoint.url('organisation')
        params = {"OrgID": org_id}

        response = requests.delete(url, headers=self._token_headers(token), params=params)
        self._check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationPathRoot...

    def find_oprs(self, token, org_id=None):
        url = MgrEndpoint.url('opr')
        params = {"OrgID": org_id} if org_id else {}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return tuple(OrganisationPathRoot.construct_from_jdict(jdict) for jdict in response.json())


    def get_opr_by_path_root(self, token, path_root):
        url = MgrEndpoint.url('opr')
        params = {"PathRoot": path_root}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return OrganisationPathRoot.construct_from_jdict(response.json())


    def insert_opr(self, token, opr):
        url = ExecEndpoint.url('opr')
        payload = JSONify.dumps(opr)

        response = requests.post(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)

        return OrganisationPathRoot.construct_from_jdict(response.json())


    def delete_opr(self, token, opr_id):
        url = ExecEndpoint.url('opr')
        params = {"OPRID": opr_id}

        response = requests.delete(url, headers=self._token_headers(token), params=params)
        self._check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationUser...

    def find_users(self, token):
        url = MgrEndpoint.url('user')

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(OrganisationUser.construct_from_jdict(jdict) for jdict in response.json())


    def find_users_by_organisation(self, token, org_id):
        url = MgrEndpoint.url('user')
        params = {"OrgID": org_id}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return tuple(OrganisationUser.construct_from_jdict(jdict) for jdict in response.json())


    def find_cognito_users_by_organisation(self, token, org_id):
        url = MgrEndpoint.url('cognito-user')
        params = {"OrgID": org_id}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return tuple(CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_users_by_username(self, token, username):
        url = MgrEndpoint.url('user')
        params = {"Username": username}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return tuple(OrganisationUser.construct_from_jdict(jdict) for jdict in response.json())


    def get_user(self, token, username, org_id):
        url = MgrEndpoint.url('user')
        params = {"Username": username, "OrgID": org_id}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return OrganisationUser.construct_from_jdict(response.json())


    def assert_user(self, token, user):
        url = MgrEndpoint.url('user')
        payload = JSONify.dumps(user)

        response = requests.post(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    def delete_user(self, token, username, org_id):
        url = ExecEndpoint.url('user')
        params = {"Username": username, "OrgID": org_id}

        response = requests.delete(url, headers=self._token_headers(token), params=params)
        self._check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationUserPath...

    def find_oups(self, token, username=None, opr_id=None):
        url = MgrEndpoint.url('oup')
        params = {}

        if username:
            params['Username'] = username

        if opr_id:
            params['OPRID'] = opr_id

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return tuple(OrganisationUserPath.construct_from_jdict(jdict) for jdict in response.json())


    def assert_oup(self, token, oup):
        url = MgrEndpoint.url('oup')
        payload = JSONify.dumps(oup)

        response = requests.post(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    def delete_oup(self, token, oup):
        url = MgrEndpoint.url('oup')
        params = {'oup': json.dumps(oup)}

        response = requests.delete(url, headers=self._token_headers(token), params=params)
        self._check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationDevice...

    def find_devices(self, token):
        url = MgrEndpoint.url('device')

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(OrganisationDevice.construct_from_jdict(jdict) for jdict in response.json())


    def find_devices_by_tag(self, token, device_tag):
        url = MgrEndpoint.url('device')
        params = {"DeviceTag": device_tag}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return tuple(OrganisationDevice.construct_from_jdict(jdict) for jdict in response.json())


    def find_devices_by_organisation(self, token, org_id):
        url = MgrEndpoint.url('device')
        params = {"OrgID": org_id}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return tuple(OrganisationDevice.construct_from_jdict(jdict) for jdict in response.json())


    def assert_device(self, token, device):
        url = ExecEndpoint.url('device')
        payload = JSONify.dumps(device)

        response = requests.post(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


    def delete_device(self, token, device):
        url = ExecEndpoint.url('device')
        payload = JSONify.dumps(device)

        response = requests.delete(url, headers=self._token_headers(token), data=payload)
        self._check_response(response)


# --------------------------------------------------------------------------------------------------------------------

class DeviceOrganisationManager(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationDevice...

    def location_path_in_use(self, token, location_path):
        params = {"LocationPath": location_path}

        response = requests.get(DevEndpoint.url(), headers=self._token_headers(token), json=params)
        self._check_response(response)

        return json.loads(response.json())
