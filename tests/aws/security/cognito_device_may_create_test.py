#!/usr/bin/env python3

"""
Created on 24 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.security.cognito_device import CognitoDeviceIdentity
from scs_core.aws.security.cognito_device_creator import CognitoDeviceCreator


# --------------------------------------------------------------------------------------------------------------------

tag = 'scs-be2-3'
shared_secret = 'WzR8dPqmuUA8yRSI'
invoice_number = 'INV-0000'

identity = CognitoDeviceIdentity(tag, shared_secret, invoice_number, None, None)

manager = CognitoDeviceCreator(requests)

response = manager.may_create(identity)
print("response: %s" % response)
