#!/usr/bin/env python3

"""
Created on 9 Feb 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.security.cognito_password_manager import CognitoPasswordResponse
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

for member in CognitoPasswordResponse:
    print("%s: %s" % (member.name, member))

print("-")

response = CognitoPasswordResponse.EmailSent
print("object: %s" % response)

jstr = JSONify.dumps(response)
print("jstr: %s" % jstr)

response = CognitoPasswordResponse.construct_from_jdict(json.loads(jstr))
print("object: %s" % response)
