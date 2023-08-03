#!/usr/bin/env python3

"""
Created on 24 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.security.cognito_device import CognitoDeviceIdentity
from scs_core.aws.security.cognito_device_creator import CognitoDeviceCreator

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

tag = 'scs-test-1'
shared_secret = '0123456789abcdef'
invoice_number = 'INV-TEST001'

credentials = CognitoDeviceIdentity(tag, shared_secret, invoice_number, None, None)
print(credentials)
print("-")

creator = CognitoDeviceCreator()
response = creator.create(credentials)
print(response)
print("-")

print(JSONify.dumps(response))
