#!/usr/bin/env python3

"""
Created on 23 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.security.cognito_login_manager import CognitoLoginManager
from scs_core.aws.security.cognito_user_credentials import CognitoUserCredentials

from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

credentials = CognitoUserCredentials('jadempage@outlook.com', 'g77!!HDsKD')
print(credentials)
print("-")

manager = CognitoLoginManager(requests)

try:
    response = manager.login(credentials)
    print(response)
except HTTPException as ex:
    print(ex)

print("=")

credentials = CognitoUserCredentials('jadempage@outlook.com', 'e77!!HDsK')
print(credentials)
print("-")

manager = CognitoLoginManager(requests)

try:
    response = manager.login(credentials)
    print(response)
except HTTPException as ex:
    print(ex.data)

