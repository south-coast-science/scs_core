#!/usr/bin/env python3

"""
Created on 4 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""
import logging

from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager
from scs_core.aws.security.organisation_manager import DeviceOrganisationManager

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

# --------------------------------------------------------------------------------------------------------------------

Logging.config('device_organisation_manager_test', verbose=True)
logging.warning(Host.__qualname__)

device_tag = 'scs-be2-3'
shared_secret = '5U4jDlG72vWu1xCE'
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

# path = None
# exists = manager.location_path_in_use(auth.id_token, path)
# print("path: %s exists: %s" % (path, exists))

