#!/usr/bin/env python3

"""
Created on 12 Oct 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


import json
import sys

from scs_analysis.cmd.cmd_alert import CmdAlert

from scs_core.aws.monitor.alert.alert import AlertSpecification

from scs_core.aws.monitor.alert.alert_specification_manager import AlertSpecificationManager
from scs_core.aws.manager.byline.byline_finder import BylineFinder

from scs_core.aws.security.cognito_client_credentials import CognitoClientCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.client.http_exception import HTTPException, HTTPNotFoundException

from scs_core.data.datum import Datum
from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict
from scs_core.data.str import Str

from scs_core.location.timezone import Timezone

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

Logging.config('alert', verbose=True)  # level=logging.DEBUG
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
    jstr = JSONify.dumps(alert)
    print("jstr: %s" % jstr)
    print("-")

    jdict = json.loads(jstr)
    print("jdict: %s" % jdict)
    print("-")

    alert = AlertSpecification.construct_from_jdict(jdict)
    print("alert: %s" % alert)
    print("-")


    response = specification_manager.update(auth.id_token, alert)
    print(response)

