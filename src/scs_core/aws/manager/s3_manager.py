"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import json
import os

from scs_core.data.path_dict import PathDict


class S3Manager(object):
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
        return bucket_list

    def retrieve_from_bucket(self, bucket_name, resource_name):
        bucket = self.__resource_client.Bucket(bucket_name)
        with open('temp_file.json', 'wb') as data:
            bucket.download_fileobj(resource_name, data)
        with open('temp_file.json', 'rb') as data:
            json_data = json.load(data)
        os.remove('temp_file.json')
        return json_data

    def upload_file_to_bucket(self, bucket_name, filepath, object_name):
        self.__resource_client.Bucket(bucket_name).upload_file(filepath, object_name)
        return "Done"
