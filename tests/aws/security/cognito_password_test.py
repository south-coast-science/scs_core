#!/usr/bin/env python3

"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.security.cognito_user import CognitoUserIdentity


# --------------------------------------------------------------------------------------------------------------------

good = 'AaBb12!%^$'
print("good: %s OK: %s" % (good, CognitoUserIdentity.is_valid_password(good)))

good = 'AaBb123|'
print("good: %s OK: %s" % (good, CognitoUserIdentity.is_valid_password(good)))

bad = 'AABB123|'
print("bad: %s OK: %s" % (bad, CognitoUserIdentity.is_valid_password(bad)))

bad = 'AaBbCcD|'
print("bad: %s OK: %s" % (bad, CognitoUserIdentity.is_valid_password(bad)))

bad = 'AaBbCc12'
print("bad: %s OK: %s" % (bad, CognitoUserIdentity.is_valid_password(bad)))

bad = 'AaBb12!%^$AaBb12!%^$AaBb12!%^$AaBb12!%^$AaBb12!%^$AaBb12!%^$AaBb12!%^$AaBb12!%^$AaBb12!%^$AaBb12!%^$AaBb12!%^$'
print("bad: %s OK: %s" % (bad, CognitoUserIdentity.is_valid_password(bad)))

bad = None
print("bad: %s OK: %s" % (bad, CognitoUserIdentity.is_valid_password(bad)))

