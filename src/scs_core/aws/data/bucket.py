"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import json
import os

import boto3


class BucketManager(object):
    # ----------------------------------------------------------------------------------------------------------------
    def __init__(self, resource_client):
        """
        Constructor
        """
        self.__client = None
        self.__resource_client = resource_client

    # ----------------------------------------------------------------------------------------------------------------
    def list_buckets(self):
        # Retrieve the list of existing buckets
        response = self.__resource_client.list_buckets()

        # Output the bucket names
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')

    def retrieve_from_bucket(self, bucket_name, resource_name):
        bucket = self.__resource_client.Bucket(bucket_name)
        with open('temp_file.json', 'wb') as data:
            bucket.download_fileobj(resource_name, data)
        with open('temp_file.json', 'rb') as data:
            json_data = json.load(data)
            print(json_data)
        os.remove('temp_file.json')

    def upload_file_to_bucket(self, bucket_name, filepath, object_name):
        self.__resource_client.Bucket(bucket_name).upload_file(filepath, object_name)


