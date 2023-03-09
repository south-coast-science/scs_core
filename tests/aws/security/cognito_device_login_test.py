#!/usr/bin/env python3

"""
Created on 21 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.security.cognito_login_manager import CognitoLoginManager
from scs_core.aws.security.cognito_device import CognitoDeviceCredentials

from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

manager = CognitoLoginManager(requests)

# --------------------------------------------------------------------------------------------------------------------

# Valid...
credentials = CognitoDeviceCredentials('scs-be2-3', 'pYL7B1JcgJ2gy6MP')
print(credentials)
print("-")

try:
    response = manager.device_login(credentials)
    print("response: %s" % response)

except HTTPException as ex:
    print(ex.data)

print("=")

# Invalid...
credentials = CognitoDeviceCredentials('scs-opc-x', 'Ytzglk6oYpzJY0FB')
print(credentials)
print("-")

manager = CognitoLoginManager(requests)

try:
    response = manager.device_login(credentials)
    print("response: %s" % response)

except HTTPException as ex:
    print(ex.data)
