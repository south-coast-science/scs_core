#!/usr/bin/env python3

"""
Created on 29 Sep 2020
@author: Jade Page (jade.page@southcoastscience.com)
Allows the user to add or view files in their buckets, as well as list all of the buckets on their account

Example usages:
aws_bucket.py -a -b scs-device-monitor -k test.txt
-f /home/jade/PycharmProjects/AWSLambdaProject/scs_core/tests/aws/data/bucket_file.txt

aws_bucket.py -l

aws_bucket.py -d -b scs-device-monitor -k test.txt
"""

# --------------------------------------------------------------------------------------------------------------------
import sys
import boto3

from getpass import getpass
from cmd.cmd_aws_bucket import CmdAWSBucketManager
from scs_core.aws.data.bucket import BucketManager


def create_aws_clients():
    access_key_secret = ""
    access_key_id = input("Enter AWS Access Key ID or leave blank to use environment variables: ")
    if access_key_id:
        access_key_secret = getpass(prompt="Enter Secret AWS Access Key: ")

    if access_key_id and access_key_secret:
        aws_client = boto3.client(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_secret,
            region_name='us-west-2'
        )
        aws_resource_client = boto3.resource(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_secret,
            region_name='us-west-2'
        )
    else:
        aws_client = boto3.client('s3', region_name='us-west-2')
        aws_resource_client = boto3.resource('s3', region_name='us-west-2')

    return aws_client, aws_resource_client


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSBucketManager()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("aws_group_setup: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()
    # ----------------------------------------------------------------------------------------------------------------
    # run...
    client, resource_client = create_aws_clients()
    bucket_manager = BucketManager(client, resource_client)
    if cmd.list_buckets:
        bucket_list = bucket_manager.list_buckets()
        print(bucket_list)

    if cmd.download:
        downloaded_resource = bucket_manager.retrieve_from_bucket(cmd.bucket_name, cmd.key_name)
        print(downloaded_resource)

    if cmd.add:
        response = bucket_manager.upload_file_to_bucket(cmd.bucket_name, cmd.filename, cmd.key_name)
        print(response)

