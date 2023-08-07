#!/usr/bin/env python3

"""
Created on 4 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager
from scs_core.aws.security.organisation_manager import DeviceOrganisationManager


# --------------------------------------------------------------------------------------------------------------------

device_tag = 'scs-be2-3'
shared_secret = 'OB1yevNUrVX0ChLE'
credentials = CognitoDeviceCredentials(device_tag, shared_secret)

gatekeeper = CognitoLoginManager()
auth = gatekeeper.device_login(credentials)
print("auth: %s" % auth.authentication_status)
print("-")

manager = DeviceOrganisationManager()

path = 'cirrusresearch/development/loc/11/'
exists = manager.location_path_in_use(auth.id_token, path)
print("path: %s exists: %s" % (path, exists))

path = 'dustscan/urban/loc/2/'
exists = manager.location_path_in_use(auth.id_token, path)
print("path: %s exists: %s" % (path, exists))

