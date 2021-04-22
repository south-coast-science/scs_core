#!/usr/bin/env python3

"""
Created on 22 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.manager.configuration_finder import ConfigurationRequest


# --------------------------------------------------------------------------------------------------------------------

MODE = ConfigurationRequest.MODE
print(ConfigurationRequest.MODE.FULL)


