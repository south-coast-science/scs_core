#!/usr/bin/env python3

"""
Created on 11 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import pytz
import requests

from scs_core.aws.data.alert import AlertSpecification, AlertStatus

from scs_core.data.diurnal_period import DiurnalPeriod
from scs_core.data.json import JSONify
from scs_core.data.recurring_period import RecurringPeriod

from scs_core.aws.manager.alert_specification_manager import AlertSpecificationManager

from scs_core.aws.security.cognito_client_credentials import CognitoClientCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------
# data...

jstr = """
"""


# --------------------------------------------------------------------------------------------------------------------

Logging.config('alert', verbose=True)
logger = Logging.getLogger()


# --------------------------------------------------------------------------------------------------------------------
# authentication...

credentials = CognitoClientCredentials.load_for_user(Host, name='super')

if not credentials:
    exit(1)

gatekeeper = CognitoLoginManager(requests)
auth = gatekeeper.user_login(credentials)

if not auth.is_ok():
    logger.error("login: %s" % auth.authentication_status.description)
    exit(1)


# ------------------------------------------------------------------------------------------------------------
# resources...

specification_manager = AlertSpecificationManager(requests)


# --------------------------------------------------------------------------------------------------------------------
# data...

alerts = specification_manager.find(auth.id_token, None, None, None, None).alerts


# --------------------------------------------------------------------------------------------------------------------
# update...

for alert in alerts:
    alert.aggregation_period.timezone = pytz.timezone('Europe/London')
    specification_manager.update(auth.id_token, alert)
    print(alert)
