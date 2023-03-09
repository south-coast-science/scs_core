#!/usr/bin/env python3

"""
Created on 23 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.security.cognito_login_manager import CognitoLoginManager
from scs_core.aws.security.cognito_user import CognitoUserCredentials

from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

manager = CognitoLoginManager(requests)

# --------------------------------------------------------------------------------------------------------------------

# Valid...
credentials = CognitoUserCredentials(None, 'production@southcoastscience.com', 'scs_admin_Password_123!', None)
print(credentials)
print("-")

try:
    response = manager.user_login(credentials)
    print("response: %s" % response)

except HTTPException as ex:
    print(ex.data)

print("=")

# Invalid...
credentials = CognitoUserCredentials(None, 'jadempage@outlook.com', 'e77!!HDsK', None)
print(credentials)
print("-")

manager = CognitoLoginManager(requests)

try:
    response = manager.user_login(credentials)
    print("response: %s" % response)

except HTTPException as ex:
    print(ex.data)
