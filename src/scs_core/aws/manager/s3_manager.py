"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

import boto3

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class S3Manager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def create_clients(cls, access_key=None):
        if access_key:
            aws_client = boto3.client(
                's3',
                aws_access_key_id=access_key.key_id,
                aws_secret_access_key=access_key.secret_key,
                region_name='us-west-2'
            )
            aws_resource_client = boto3.resource(
                's3',
                aws_access_key_id=access_key.key_id,
                aws_secret_access_key=access_key.secret_key,
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
        response = self.__client.list_buckets()

        return [Bucket.construct(bucket) for bucket in response['Buckets']]


    def retrieve_from_bucket(self, bucket_name, resource_name):
        response = self.__client.get_object(Bucket=bucket_name, Key=resource_name)
        content_body = response.get("Body")
        data = content_body.read()

        return data.decode()


    def upload_file_to_bucket(self, bucket_name, filepath, key_name):
        self.__resource_client.Bucket(bucket_name).upload_file(filepath, key_name)


    def upload_bytes_to_bucket(self, bucket_name, body, key_name):
        self.__client.Bucket(bucket_name).put_object(Body=body, Key=key_name)


    def put_object(self, bucket_name, body, key_name):
        self.__client.put_object(Body=body, Bucket=bucket_name, Key=key_name)


    def list_bucket_objects(self, bucket_name):
        response = self.__client.list_objects_v2(
            Bucket=bucket_name,
            Delimiter=",",
        )

        return [Object.construct(item) for item in response['Contents']]


# --------------------------------------------------------------------------------------------------------------------

class Bucket(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, response):
        name = response.get('Name')
        creation_date = LocalizedDatetime(response.get('CreationDate'))

        return cls(name, creation_date)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, creation_date):
        """
        Constructor
        """
        self.__name = name                                  # string
        self.__creation_date = creation_date                # LocalizedDatetime


    def __lt__(self, other):
        return self.name < other.name


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['name'] = self.name
        jdict['creation-date'] = self.creation_date.as_iso8601()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def creation_date(self):
        return self.__creation_date


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Bucket:{name:%s, creation_date:%s}" %  (self.name, self.creation_date)


# --------------------------------------------------------------------------------------------------------------------

class Object(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, response):
        key = response.get('Key')
        last_modified = LocalizedDatetime(response.get('LastModified'))
        e_tag = response.get('ETag')
        size = response.get('Size')
        storage_class = response.get('StorageClass')

        return cls(key, last_modified, e_tag, size, storage_class)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, key, last_modified, e_tag, size, storage_class):
        """
        Constructor
        """
        self.__key = key                                    # string
        self.__last_modified = last_modified                # LocalizedDatetime
        self.__e_tag = e_tag                                # string
        self.__size = int(size)                             # int
        self.__storage_class = storage_class                # string


    def __lt__(self, other):
        if self.key < other.key:
            return True

        return self.e_tag < other.e_tag


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['key'] = self.key
        jdict['last-modified'] = self.last_modified.as_iso8601()
        jdict['e-tag'] = self.e_tag
        jdict['size'] = self.size
        jdict['storage-class'] = self.storage_class

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def key(self):
        return self.__key


    @property
    def last_modified(self):
        return self.__last_modified


    @property
    def e_tag(self):
        return self.__e_tag


    @property
    def size(self):
        return self.__size


    @property
    def storage_class(self):
        return self.__storage_class


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Object:{key:%s, last_modified:%s, e_tag:%s, size:%s, storage_class:%s}" % \
               (self.key, self.last_modified, self.e_tag, self.size, self.storage_class)
