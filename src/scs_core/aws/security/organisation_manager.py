"""
Created on 17 Jan 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from http import HTTPStatus

from scs_core.aws.security.organisation import Organisation, OrganisationPathRoot, OrganisationUser, \
    OrganisationUserPath, OrganisationDevice

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class OrganisationManager(object):
    """
    classdocs
    """

    __URL = "https://mmkduy8i4l.execute-api.us-west-2.amazonaws.com/default/OrganisationManager"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __headers(cls, token):
        return {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json", "Token": token}


    @classmethod
    def __check_response(cls, response):
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException(status.value, response.reason, response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        self.__http_client = http_client                # requests package
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------
    # Organisation...

    def find_organisations(self, token):
        url = '/'.join((self.__URL, 'organisation'))

        response = self.__http_client.get(url, headers=self.__headers(token))
        self.__check_response(response)

        return [Organisation.construct_from_jdict(jdict) for jdict in response.json()]


    def get_organisation_by_label(self, token, label):
        url = '/'.join((self.__URL, 'organisation'))
        payload = json.dumps({"Label": label})

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return Organisation.construct_from_jdict(response.json())


    def insert_organisation(self, token, organisation):
        url = '/'.join((self.__URL, 'organisation'))
        payload = json.dumps(organisation)

        response = self.__http_client.post(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return Organisation.construct_from_jdict(response.json())


    def update_organisation(self, token, organisation):
        url = '/'.join((self.__URL, 'organisation'))
        payload = json.dumps(organisation)

        response = self.__http_client.patch(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)


    def delete_organisation(self, token, label):
        url = '/'.join((self.__URL, 'organisation'))
        payload = json.dumps({"Label": label})

        response = self.__http_client.delete(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationPathRoot...

    def find_oprs_by_organisation(self, token, org_id):
        url = '/'.join((self.__URL, 'opr'))
        payload = json.dumps({"OrgID": org_id})

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return [OrganisationPathRoot.construct_from_jdict(jdict) for jdict in response.json()]


    def insert_opr(self, token, opr):
        url = '/'.join((self.__URL, 'opr'))
        payload = json.dumps(opr)

        response = self.__http_client.post(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return OrganisationPathRoot.construct_from_jdict(response.json())


    def delete_opr(self, token, opr_id):
        url = '/'.join((self.__URL, 'opr'))
        payload = json.dumps({"OPRID": opr_id})

        response = self.__http_client.delete(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationUser...

    def find_users_by_organisation(self, token, org_id):
        url = '/'.join((self.__URL, 'user'))
        payload = json.dumps({"OrgID": org_id})

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return [OrganisationUser.construct_from_jdict(jdict) for jdict in response.json()]


    def find_users_by_username(self, token, username):
        url = '/'.join((self.__URL, 'user'))
        payload = json.dumps({"Username": username})

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return [OrganisationUser.construct_from_jdict(jdict) for jdict in response.json()]


    def get_user(self, token, username, org_id):
        url = '/'.join((self.__URL, 'user'))
        payload = json.dumps({"Username": username, "OrgID": org_id})

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return OrganisationUser.construct_from_jdict(response.json())


    def assert_user(self, token, user):
        url = '/'.join((self.__URL, 'user'))
        payload = json.dumps(user)

        response = self.__http_client.post(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationUserPath...

    def find_oup_by_user(self, token, username):
        url = '/'.join((self.__URL, 'oup'))
        payload = json.dumps({"Username": username})

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return [OrganisationUserPath.construct_from_jdict(jdict) for jdict in response.json()]


    def assert_oup(self, token, oup):
        url = '/'.join((self.__URL, 'oup'))
        payload = json.dumps(oup)

        response = self.__http_client.post(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)


    def delete_oup(self, token, oup):
        url = '/'.join((self.__URL, 'oup'))
        payload = json.dumps(oup)

        response = self.__http_client.delete(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)


    # ----------------------------------------------------------------------------------------------------------------
    # OrganisationDevice...

    def find_devices_by_tag(self, token, device_tag):
        url = '/'.join((self.__URL, 'device'))
        payload = json.dumps({"DeviceTag": device_tag})

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return [OrganisationDevice.construct_from_jdict(jdict) for jdict in response.json()]


    def find_devices_by_organisation(self, token, org_id):
        url = '/'.join((self.__URL, 'device'))
        payload = json.dumps({"OrgID": org_id})

        response = self.__http_client.get(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)

        return [OrganisationDevice.construct_from_jdict(jdict) for jdict in response.json()]


    def assert_device(self, token, device):
        url = '/'.join((self.__URL, 'device'))
        payload = json.dumps(device)

        response = self.__http_client.post(url, data=payload, headers=self.__headers(token))
        self.__check_response(response)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OrganisationManager:{rest_client:%s}" % self.__http_client
