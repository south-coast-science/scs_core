#!/usr/bin/env python3

"""
Created on 20 Jan 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.security.cognito_login_manager import CognitoUserLoginManager
from scs_core.aws.security.cognito_user import CognitoUserCredentials

from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

jstr = '''[{"Name": "sub", "Value": "332351ef-f74f-4cb4-aec8-664a3a9abae3"}, 
{"Name": "custom:tester", "Value": "False"}, {"Name": "custom:super", "Value": "False"}, 
{"Name": "email", "Value": "adrian@em-monitors.co.uk"}]'''

print(jstr)
print("-")

jdict = json.loads(jstr)
print(jstr)
print("-")


