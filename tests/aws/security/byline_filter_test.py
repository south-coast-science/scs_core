#!/usr/bin/env python3

"""
Created on 31 Oct 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.security.byline_filter import BylineFilter


# --------------------------------------------------------------------------------------------------------------------

guardian = BylineFilter(['ricardo/heathrow/loc/1/', 'ricardo/gatwick/'])
print(guardian)

bylines = [
    {'topic': 'scs/brighton/loc/1/gases'},
    {'topic': 'ricardo/heathrow/loc/1/gases'},
    {'topic': 'ricardo/heathrow/loc/2/gases'},
    {'topic': 'ricardo/gatwick/loc/1/gases'},
    {'topic': 'ricardo/luton/loc/1/gases'}
]

for visible in guardian.filter(bylines):
    print(visible)

