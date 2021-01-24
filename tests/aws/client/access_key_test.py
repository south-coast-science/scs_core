#!/usr/bin/env python3

"""
Created on 24 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

./access_key_test.py

./access_key_test.py

"""

from scs_core.aws.client.access_key import AccessKey


# --------------------------------------------------------------------------------------------------------------------

key = AccessKey.from_user()
print(key)
