#!/usr/bin/env python3

"""
Created on 5 Jul 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.greengrass.v1.aws_group_version import AWSGroupVersion

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

group = AWSGroupVersion.load(Host)
print(group)
print("-")

print(group.as_json())
print("-")

print("core: %s" % group.core)
print("core_arn: %s" % group.core_arn)
print("core_name: %s" % group.core_name)
print("group_name: %s" % group.group_name)
print("-")

print("loggers: %s" % group.loggers)
print("-")

print("greengrass_log_level: %s" % group.greengrass_log_level)
group.greengrass_log_level = 'DEBUG'
print("-")

print("lambda_log_level: %s" % group.lambda_log_level)
group.lambda_log_level = 'WARN'
print("-")

group.save(Host)


