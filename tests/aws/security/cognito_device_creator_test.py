#!/usr/bin/env python3

"""
Created on 24 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_device_creator import CognitoDeviceCreator

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

tag = 'scs-test-1'
shared_secret = '0123456789abcdef'

credentials = CognitoDeviceCredentials(tag, shared_secret)
print(credentials)
print("-")

creator = CognitoDeviceCreator(requests)
response = creator.create(credentials)
print(response)
print("-")

print(JSONify.dumps(response))
