#!/usr/bin/env python3

"""
Created on 21 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.security.cognito_login_manager import CognitoDeviceLoginManager
from scs_core.aws.security.cognito_device import CognitoDeviceCredentials

from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

credentials = CognitoDeviceCredentials('scs-opc-1', 'Ytzglk6oYpzJY0FB')
print(credentials)
print("-")

manager = CognitoDeviceLoginManager(requests)

try:
    response = manager.login(credentials)
    print(response)
except HTTPException as ex:
    print(ex.data)

print("=")

credentials = CognitoDeviceCredentials('scs-opc-x', 'Ytzglk6oYpzJY0FB')
print(credentials)
print("-")

manager = CognitoDeviceLoginManager(requests)

try:
    response = manager.login(credentials)
    print(response)
except HTTPException as ex:
    print(ex.data)

