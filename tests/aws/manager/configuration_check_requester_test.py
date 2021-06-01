#!/usr/bin/env python3

"""
Created on 26 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.manager.configuration_check_requester import ConfigurationCheckRequester


# --------------------------------------------------------------------------------------------------------------------

requester = ConfigurationCheckRequester(requests, None)
print(requester)
print("-")

response = requester.request('scs-bgx-401')
print(response)

response = requester.request('scs-unknown')
print(response)

