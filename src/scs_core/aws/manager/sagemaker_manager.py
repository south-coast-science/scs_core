"""
Created on 04 Dec 2020

@author: Jade Page (jade.page@southcoastscience.com)

Case insensitive starts with solution:
https://stackoverflow.com/questions/13578916/case-insensitive-string-startswith-in-python
"""
import boto3


class SagemakerManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def create_clients(cls, access_key=None):
        if access_key:
            client = boto3.client(
                'sagemaker',
                aws_access_key_id=access_key.key_id,
                aws_secret_access_key=access_key.secret_key,
                region_name='us-west-2'
            )

        else:
            client = boto3.client('sagemaker', region_name='us-west-2')

        return client

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client):
        """
        Constructor
        """
        self.__client = client

    @staticmethod
    def starts_with(a_source: str, a_prefix: str) -> bool:
        source_prefix = a_source[:len(a_prefix)]
        return source_prefix.casefold() == a_prefix.casefold()

    def delete_models_with_prefix(self, prefix):
        deletion_list = self.list_model_names_prefix(prefix)
        deleted = 0
        for item in deletion_list:
            response = self.__client.delete_model(
                ModelName=item
            )
            deleted += 1
        return deleted

    def list_model_names_prefix(self, prefix):
        result = []
        names = self.list_model_names_filter(prefix)
        for item in names:
            if self.starts_with(item, prefix):
                result.append(item)

        return result


    def list_model_names_filter(self, filter):
        names = []
        response = []
        next_token = None
        should_continue = True

        while should_continue:
            res, next_token = self.retrieve_filtered_models(filter, next_token)
            response.append(res)
            models = res.get("Models")
            for item in models:
                name = item.get("ModelName")
                names.append(name)
            if not next_token:
                should_continue = False

        return names

    def list_model_names(self):
        names = []
        response = []
        next_token = None
        should_continue = True

        while should_continue:
            res, next_token = self.retrieve_models(next_token)
            response.append(res)
            models = res.get("Models")
            for item in models:
                name = item.get("ModelName")
                names.append(name)
            if not next_token:
                should_continue = False

        return names

    def retrieve_models(self, next_token=None):
        next_token2 = None

        if next_token:
            response = self.__client.list_models(
                SortBy='Name',
                SortOrder='Descending',
                MaxResults=100,
                NextToken=next_token
            )
        else:
            response = self.__client.list_models(
                SortBy='Name',
                SortOrder='Descending',
                MaxResults=100
            )

        if "NextToken" in response:
            next_token2 = response.get("NextToken")

        return response, next_token2

    def retrieve_filtered_models(self, filter_string, next_token=None):
        next_token2 = None

        if next_token:
            response = self.__client.list_models(
                SortBy='Name',
                SortOrder='Descending',
                MaxResults=100,
                NameContains = filter_string,
                NextToken=next_token
            )
        else:
            response = self.__client.list_models(
                SortBy='Name',
                SortOrder='Descending',
                MaxResults=100,
                NameContains=filter_string
            )

        if "NextToken" in response:
            next_token2 = response.get("NextToken")

        return response, next_token2

