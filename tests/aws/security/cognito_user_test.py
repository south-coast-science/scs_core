#!/usr/bin/env python3

"""
Created on 27 Feb 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.security.cognito_user import CognitoUserIdentity

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

username = 123
created = round(LocalizedDatetime.now(), 3)
confirmation_status = CognitoUserIdentity.status('C')
enabled = True
email_verified = False
email = 'bruno.beloff@southcoastscience.com'
given_name = 'Bruno'
family_name = 'Beloff'
password = 'ABCxyz123!'
is_super = True
is_tester = False
is_financial = False

identity1 = CognitoUserIdentity(username, created, confirmation_status, enabled, email_verified, email,
                                given_name, family_name, password, is_super, is_tester, is_financial, None)
print(identity1)

jstr = JSONify.dumps(identity1)
print(jstr)
print("-")

identity2 = CognitoUserIdentity.construct_from_jdict(json.loads(jstr))
print(identity2)
print("-")

print("equals: %s" % str(identity1 == identity2))
