#!/usr/bin/env python3

"""
Created on 25 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.security.cognito_device_creator import CognitoDeviceCreator


# --------------------------------------------------------------------------------------------------------------------

tag = 'scs-be2-3'

manager = CognitoDeviceCreator(requests)

response = manager.may_create(tag)
print("response: %s" % response)
