#!/usr/bin/env python3

"""
Created on 22 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.manager.configuration_finder import ConfigurationRequest


# --------------------------------------------------------------------------------------------------------------------

mode = ConfigurationRequest.Mode
print(mode)

mode = mode['TAGS_ONLY']
print(mode.name)

request = ConfigurationRequest(None, False, mode)
print(request)

print(request.tags_only())
