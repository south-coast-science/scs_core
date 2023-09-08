#!/usr/bin/env python3

"""
Created on 18 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.security.organisation import Organisation


# --------------------------------------------------------------------------------------------------------------------

users = ['someone@somewhere.com', 'bruno.beloff@southcoastscience.com', 'paul@p3d.co.uk', 'another@domain.com']

org = Organisation(1, '4fsera', None, None, None, None)
filtered_users = org.filtered_users(users)
print(filtered_users)
print("-")

org = Organisation(1, 'South Coast Science (Dev)', None, None, None, None)
filtered_users = org.filtered_users(users)
print(filtered_users)
