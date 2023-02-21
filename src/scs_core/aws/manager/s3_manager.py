"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

from botocore.exceptions import ClientError
from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.tokens import Tokens

from scs_core.sys.persistence_manager import PersistenceManager


# --------------------------------------------------------------------------------------------------------------------

class S3Manager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client, resource_client):
        """
        Constructor
        """
        self.__client = client
        self.__resource_client = resource_client


    # ----------------------------------------------------------------------------------------------------------------

    def list_buckets(self, full_details):
        response = self.__client.list_buckets()

        if 'Buckets' not in response:
            return

        for bucket in response['Buckets']:
            yield Bucket.construct(bucket) if full_details else bucket['Name']


    def list_objects(self, bucket, depth, full_details, prefix=None):
        prefix_tokens = None if prefix is None else Tokens.construct(prefix, '/')
        next_token = None
        summary = Summary.none()

        while True:
            response = self.__retrieve_objects(bucket, prefix, next_token)

            if not response or 'Contents' not in response:
                return

            for item in response['Contents']:
                key_tokens = Tokens.construct(item['Key'], '/')

                if prefix is None or key_tokens.startswith(prefix_tokens):
                    # full...
                    if full_details:
                        yield Object.construct(item)
                        continue

                    # minimal...
                    if depth is None:
                        yield item['Key']
                        continue

                    # summary...
                    path = key_tokens.path(depth=depth)
                    obj = Object.construct(item)

                    if path == summary.path:
                        summary.add(obj)
                        continue

                    if not summary.is_none():
                        yield summary

                    summary = Summary.new(path, obj)

            if 'NextContinuationToken' not in response:
                break

            next_token = response.get('NextContinuationToken')

        if summary.path is not None:
            yield summary


    def retrieve_from_bucket(self, bucket, key):
        response = self.__client.get_object(Bucket=bucket, Key=key)

        meta = response.get('ResponseMetadata')
        header = meta.get('HTTPHeaders')
        last_modified = LocalizedDatetime.construct_from_s3(header.get('last-modified'))

        content_body = response.get("Body")
        data = content_body.read().decode()

        return data, last_modified


    def upload_file_to_bucket(self, filepath, bucket, key):
        self.__resource_client.Bucket(bucket).upload_file(filepath, key)

        return self.head(bucket, key)


    def upload_bytes_to_bucket(self, body, bucket, key):
        self.__resource_client.Bucket(bucket).put_object(Body=body, Key=key)

        return self.head(bucket, key)


    def put_object(self, body, bucket, key):
        self.__client.put_object(Body=body, Bucket=bucket, Key=key)

        return self.head(bucket, key)


    def move_object(self, bucket, key, new_key):
        source = '/'.join((bucket, key))

        self.__client.copy_object(Bucket=bucket, CopySource=source, Key=new_key)
        self.__client.delete_object(Bucket=bucket, Key=key)

        return self.head(bucket, new_key)


    def delete_objects(self, bucket, prefix, excluded=None):
        excluded_tokens = Tokens.construct(excluded, '/')

        for key in self.list_objects(bucket, None, False, prefix=prefix):
            if excluded and Tokens.construct(key, '/').startswith(excluded_tokens):
                continue

            self.delete_object(bucket, key)
            yield key


    def delete_object(self, bucket, key):
        self.__client.delete_object(Bucket=bucket, Key=key)


    def exists(self, bucket, key):
        try:
            self.head(bucket, key)
            return True

        except ClientError as ex:
            if ex.response['Error']['Code'] == "404":
                return False

            raise


    def head(self, bucket, key):
        response = self.__client.head_object(Bucket=bucket, Key=key)
        return Head.construct(key, response)


    # ----------------------------------------------------------------------------------------------------------------

    def __retrieve_objects(self, bucket, prefix, next_token):
        if prefix:
            if next_token:
                response = self.__client.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                    ContinuationToken=next_token,
                    Delimiter=",",
                )
            else:
                response = self.__client.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                    Delimiter=",",
                )

        else:
            if next_token:
                response = self.__client.list_objects_v2(
                    Bucket=bucket,
                    ContinuationToken=next_token,
                    Delimiter=",",
                )
            else:
                response = self.__client.list_objects_v2(
                    Bucket=bucket,
                    Delimiter=",",
                )

        return response


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
    def __key(dirname, filename):
        return '/'.join((dirname, filename))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client, resource_client):
        """
        Constructor
        """
        self.__manager = S3Manager(client, resource_client)


    # ----------------------------------------------------------------------------------------------------------------

    def list(self, container, dirname):
        prefix_len = len(dirname) + 1
        objects = self.__manager.list_objects(container, 1, True, prefix=dirname)

        return tuple(obj.key[prefix_len:] for obj in objects)


    def exists(self, dirname, filename):
        key = self.__key(dirname, filename)

        return self.__manager.exists(self.__BUCKET, key)


    def load(self, dirname, filename, encryption_key=None):
        key = self.__key(dirname, filename)

        text, last_modified = self.__manager.retrieve_from_bucket(self.__BUCKET, key)

        if encryption_key:
            from scs_core.data.crypt import Crypt               # late import
            jstr = Crypt.decrypt(encryption_key, text)
        else:
            jstr = text

        return jstr, last_modified


    def save(self, jstr, dirname, filename, encryption_key=None):
        key = self.__key(dirname, filename)

        if encryption_key:
            from scs_core.data.crypt import Crypt               # late import
            text = Crypt.encrypt(encryption_key, jstr)
        else:
            text = jstr + '\n'

        self.__manager.put_object(text, self.__BUCKET, key)


    def remove(self, dirname, filename):
        key = self.__key(dirname, filename)

        self.__manager.delete_object(self.__BUCKET, key)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def scs_path(cls):
        return cls.__BUCKET


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
        return "Bucket:{name:%s, creation_date:%s}" % (self.name, self.creation_date)


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


# --------------------------------------------------------------------------------------------------------------------

class Summary(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def none(cls):
        return cls(None, 0, None, 0)


    @classmethod
    def new(cls, path, obj: Object):
        return cls(path, 1, obj.last_modified, obj.size)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, objects, last_modified, size):
        """
        Constructor
        """
        self.__path = path                                  # string
        self.__objects = int(objects)                       # int
        self.__last_modified = last_modified                # LocalizedDatetime
        self.__size = int(size)                             # int


    def __lt__(self, other):
        return self.path < other.path


    # ----------------------------------------------------------------------------------------------------------------

    def is_none(self):
        return self.path is None


    def add(self, obj: Object):
        self.__objects += 1

        if self.last_modified is None or obj.last_modified > self.last_modified:
            self.__last_modified = obj.last_modified

        self.__size += obj.size


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['path'] = self.path
        jdict['objects'] = self.objects
        jdict['last-modified'] = self.last_modified.as_iso8601()
        jdict['size'] = self.size

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


    @property
    def objects(self):
        return self.__objects


    @property
    def last_modified(self):
        return self.__last_modified


    @property
    def size(self):
        return self.__size


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Summary:{path:%s, objects:%s, last_modified:%s, size:%s}" %  \
               (self.path, self.objects, self.last_modified, self.size)
