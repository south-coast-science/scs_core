#!/usr/bin/env python3

"""
Created on 25 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.security.cognito_device_creator import CognitoDeviceCreator
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

Logging.config('cognito_device_may_create_test', verbose=True)


tag = 'scs-be2-3'

manager = CognitoDeviceCreator()

response = manager.may_create(tag)
print("response: %s" % response)
