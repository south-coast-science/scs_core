#!/usr/bin/env python3

"""
Created on 20 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datum import Datum


# --------------------------------------------------------------------------------------------------------------------

email = 'bbeloff@me.com'
print("email: %s valid: %s" % (email, Datum.is_email_address(email)))

email = 'bbeloff@me.co.uk'
print("email: %s valid: %s" % (email, Datum.is_email_address(email)))
print("-")

email = 'bbeloff@me'
print("email: %s valid: %s" % (email, Datum.is_email_address(email)))

email = 'bbeloff @me.com'
print("email: %s valid: %s" % (email, Datum.is_email_address(email)))

email = 'bbeloff@me. com'
print("email: %s valid: %s" % (email, Datum.is_email_address(email)))

email = 'bbeloff@@me.com'
print("email: %s valid: %s" % (email, Datum.is_email_address(email)))

email = ''
print("email: %s valid: %s" % (email, Datum.is_email_address(email)))

email = None
print("email: %s valid: %s" % (email, Datum.is_email_address(email)))

