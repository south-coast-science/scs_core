#!/usr/bin/env python3

"""
Created on 6 Mar 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

WARNING: run cognito_device_creator_test.py before running this script
"""

from scs_core.aws.security.access_key_manager import AccessKeyManager
from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host                  # required to init endpoints

# --------------------------------------------------------------------------------------------------------------------

Logging.config('acces_key_manager_test', verbose=True)
logger = Logging.getLogger()

logger.info("host: %s" % Host.__module__)

# credentials...
tag = 'scs-test-1'
shared_secret = '0123456789abcdef'

credentials = CognitoDeviceCredentials(tag, shared_secret)
print(credentials)
print("-")

# AccessKey...
gatekeeper = CognitoLoginManager()
auth = gatekeeper.device_login(credentials)
print(auth)
print("-")

if not auth.is_ok():
    logger.error(auth.authentication_status.description)
    exit(1)

manager = AccessKeyManager()
key = manager.get(auth.id_token)
print(key)
