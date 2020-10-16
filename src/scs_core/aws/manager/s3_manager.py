"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

import boto3
import os

from scs_core.aws.client.access_keys import AccessKeys
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class S3Manager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def create_clients(cls):
        access_key_id, access_key_secret = AccessKeys.get()

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


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client, resource_client):
        """
        Constructor
        """
        self.__client = client
        self.__resource_client = resource_client


    # ----------------------------------------------------------------------------------------------------------------

    def list_buckets(self):
        # Retrieve the list of existing buckets
        response = self.__client.list_buckets()
        bucket_list = PathDict()
        # Output the bucket names
        inters = 0
        print('Existing buckets:')
        for bucket in response['Buckets']:
            bucket_list.append(str(inters), bucket["Name"])
            inters += 1

        return response


    def retrieve_from_bucket(self, bucket_name, resource_name):
        response = self.__client.get_object(Bucket=bucket_name, Key=resource_name)
        content_body = response.get("Body")
        data = content_body.read()

        return data.decode('utf-8')


    def upload_file_to_bucket(self, bucket_name, filepath, key_name):
        self.__resource_client.Bucket(bucket_name).upload_file(filepath, key_name)

        return "Done"


    def upload_bytes_to_bucket(self, bucket_name, body, key_name):
        self.__client.Bucket(bucket_name).put_object(Body=body, Key=key_name)

        return "Done"


    def put_object(self, bucket_name, body, key_name):
        self.__client.put_object(Body=body, Bucket=bucket_name, Key=key_name)


    def list_bucket_objects(self, bucket_name):
        response = self.__client.list_objects_v2(
            Bucket=bucket_name,
            Delimiter=",",
        )

        return response
