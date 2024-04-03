#!/usr/bin/env python3

"""
Created on 24 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

WARNING: add device to whitelist before running this script
"""

from scs_core.aws.security.cognito_device import CognitoDeviceIdentity
from scs_core.aws.security.cognito_device_creator import CognitoDeviceCreator

from scs_core.data.json import JSONify

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

Logging.config('cognito_device_creator_test', verbose=True)


tag = 'scs-test-1'
shared_secret = '0123456789abcdef'
invoice_number = 'INV-0000'

credentials = CognitoDeviceIdentity(tag, password=shared_secret, invoice_number=invoice_number)
print(credentials)
print("-")

creator = CognitoDeviceCreator()
response = creator.create(credentials)
print(response)
print("-")

print(JSONify.dumps(response))
