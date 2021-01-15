"""
Created on 15 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import boto3

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.config.aws import AWS


# --------------------------------------------------------------------------------------------------------------------

class Client(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, category, key: AccessKey):
        if key.ok():
            return boto3.client(
                category,
                aws_access_key_id=key.id,
                aws_secret_access_key=key.secret,
                region_name=AWS.region()
            )

        return boto3.client(category, region_name=AWS.region())


    @classmethod
    def resource(cls, category, key: AccessKey):
        if key.ok():
            return boto3.resource(
                category,
                aws_access_key_id=key.id,
                aws_secret_access_key=key.secret,
                region_name=AWS.region()
            )

        return boto3.resource(category, region_name=AWS.region())
