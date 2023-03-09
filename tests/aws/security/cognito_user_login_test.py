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

credentials = CognitoUserCredentials(None, 'testBB@test.com', 'scs_admin_TEST_8294', 'scs_admin_TEST_8294')
print(credentials)
print("-")

manager = CognitoLoginManager(requests)

try:
    response = manager.user_login(credentials)
    print(response)
except HTTPException as ex:
    print(ex.data)

print("=")

credentials = CognitoUserCredentials(None, 'jadempage@outlook.com', 'e77!!HDsK', 'g77!!HDsKD')
print(credentials)
print("-")

manager = CognitoLoginManager(requests)

try:
    response = manager.user_login(credentials)
    print(response)
except HTTPException as ex:
    print(ex.data)

