"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

import boto3

from botocore.exceptions import ClientError

from collections import OrderedDict

from scs_core.data.crypt import Crypt
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable

from scs_core.sys.persistence_manager import PersistenceManager


# --------------------------------------------------------------------------------------------------------------------

class S3Manager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def create_clients(cls, access_key=None):
        if access_key:
            client = boto3.client(
                's3',
                aws_access_key_id=access_key.key_id,
                aws_secret_access_key=access_key.secret_key,
                region_name='us-west-2'
            )
            resource_client = boto3.resource(
                's3',
                aws_access_key_id=access_key.key_id,
                aws_secret_access_key=access_key.secret_key,
                region_name='us-west-2'
            )

        else:
            client = boto3.client('s3', region_name='us-west-2')
            resource_client = boto3.resource('s3', region_name='us-west-2')

        return client, resource_client


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

        if 'Buckets' not in response:
            return []

        return [Bucket.construct(bucket) for bucket in response['Buckets']]


    def list_objects(self, bucket_name):
        response = self.__client.list_objects_v2(
            Bucket=bucket_name,
            Delimiter=",",
        )

        if 'Contents' not in response:
            return []

        return [Object.construct(item) for item in response['Contents']]


    def retrieve_from_bucket(self, bucket_name, key_name):
        response = self.__client.get_object(Bucket=bucket_name, Key=key_name)
        content_body = response.get("Body")
        data = content_body.read()

        return data.decode()


    def upload_file_to_bucket(self, filepath, bucket_name, key_name):
        self.__resource_client.Bucket(bucket_name).upload_file(filepath, key_name)

        return self.head(bucket_name, key_name)


    def upload_bytes_to_bucket(self, body, bucket_name, key_name):
        self.__resource_client.Bucket(bucket_name).put_object(Body=body, Key=key_name)

        return self.head(bucket_name, key_name)


    def put_object(self, body, bucket_name, key_name):
        self.__client.put_object(Body=body, Bucket=bucket_name, Key=key_name)

        return self.head(bucket_name, key_name)


    def move_object(self, bucket_name, key_name, new_key_name):
        source = '/'.join((bucket_name, key_name))

        self.__client.copy_object(Bucket=bucket_name, CopySource=source, Key=new_key_name)
        self.__client.delete_object(Bucket=bucket_name, Key=key_name)

        return self.head(bucket_name, new_key_name)


    def delete_object(self, bucket_name, key_name):
        self.__client.delete_object(Bucket=bucket_name, Key=key_name)


    def exists(self, bucket_name, key_name):
        try:
            self.head(bucket_name, key_name)
            return True

        except ClientError as ex:
            if ex.response['Error']['Code'] == "404":
                return False

            raise


    def head(self, bucket_name, key_name):
        response = self.__client.head_object(Bucket=bucket_name, Key=key_name)
        return Head.construct(key_name, response)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "S3Manager:{client:%s, resource_client:%s}" % (self.__client, self.__resource_client)


# --------------------------------------------------------------------------------------------------------------------

class S3PersistenceManager(PersistenceManager):
    """
    classdocs
    """

    __BUCKET = 'scs-persistence'

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __key_name(dirname, filename):
        return '/'.join((dirname, filename))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client, resource_client):
        """
        Constructor
        """
        self.__manager = S3Manager(client, resource_client)


    # ----------------------------------------------------------------------------------------------------------------

    def exists(self, dirname, filename):
        key_name = self.__key_name(dirname, filename)

        return self.__manager.exists(self.__BUCKET, key_name)


    def load(self, dirname, filename, encryption_key=None):
        key_name = self.__key_name(dirname, filename)

        text = self.__manager.retrieve_from_bucket(self.__BUCKET, key_name)
        jstr = text if encryption_key is None else Crypt.decrypt(encryption_key, text)

        return jstr


    def save(self, jstr, dirname, filename, encryption_key=None):
        key_name = self.__key_name(dirname, filename)

        text = jstr + '\n' if encryption_key is None else Crypt.encrypt(encryption_key, jstr)

        self.__manager.put_object(text, self.__BUCKET, key_name)


    def remove(self, dirname, filename):
        key_name = self.__key_name(dirname, filename)

        self.__manager.delete_object(self.__BUCKET, key_name)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "S3PersistenceManager:{manager:%s}" % self.__manager


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

class Head(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, key, response):
        last_modified = LocalizedDatetime(response.get('LastModified'))
        e_tag = response.get('ETag')
        size = response.get('ContentLength')
        content_type = response.get('ContentType')

        return cls(key, last_modified, e_tag, size, content_type)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, key, last_modified, e_tag, size, content_type):
        """
        Constructor
        """
        self.__key = key                                    # string
        self.__last_modified = last_modified                # LocalizedDatetime
        self.__e_tag = e_tag                                # string
        self.__size = int(size)                             # int
        self.__content_type = content_type                  # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['key'] = self.key
        jdict['last-modified'] = self.last_modified.as_iso8601()
        jdict['e-tag'] = self.e_tag
        jdict['size'] = self.size
        jdict['storage-class'] = self.content_type

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
    def content_type(self):
        return self.__content_type


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Head:{key:%s, last_modified:%s, e_tag:%s, size:%s, content_type:%s}" % \
               (self.key, self.last_modified, self.e_tag, self.size, self.content_type)


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
