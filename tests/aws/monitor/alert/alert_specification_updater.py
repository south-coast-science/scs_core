#!/usr/bin/env python3

"""
Created on 12 Oct 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.monitor.alert.alert_specification_manager import AlertSpecificationManager
from scs_core.aws.manager.byline.byline_finder import BylineFinder

from scs_core.aws.security.cognito_client_credentials import CognitoClientCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

Logging.config('alert', verbose=True)
logger = Logging.getLogger()


# ------------------------------------------------------------------------------------------------------------
# authentication...

credentials = CognitoClientCredentials.load_for_user(Host, name='super')

if not credentials:
    exit(1)

gatekeeper = CognitoLoginManager()
auth = gatekeeper.user_login(credentials)

if not auth.is_ok():
    logger.error("login: %s." % auth.authentication_status.description)
    exit(1)


# ------------------------------------------------------------------------------------------------------------
# resources...

byline_finder = BylineFinder()
specification_manager = AlertSpecificationManager()


# ------------------------------------------------------------------------------------------------------------
# run...

response = specification_manager.find(auth.id_token, None, None, None, None)

for alert in sorted(response.alerts):
    response = specification_manager.update(auth.id_token, alert)
    print(response)

