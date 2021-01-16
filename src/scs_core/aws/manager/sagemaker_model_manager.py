"""
Created on 04 Dec 2020

@author: Jade Page (jade.page@southcoastscience.com)

Case insensitive starts with solution:
https://stackoverflow.com/questions/13578916/case-insensitive-string-startswith-in-python
"""


# --------------------------------------------------------------------------------------------------------------------

class SagemakerModelManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client):
        """
        Constructor
        """
        self.__client = client


    # ----------------------------------------------------------------------------------------------------------------

    def get_models(self, prefix):
        model_list = self.list_model_names_prefix(prefix, None)
        models = []

        for item in model_list:
            res = self.__client.describe_model(
                ModelName=item
            )
            models.append(res)

        return models


    def delete_models_with_prefix(self, prefix):
        deletion_list = self.list_model_names_prefix(prefix, None)

        for item in deletion_list:
            self.__client.delete_model(
                ModelName=item
            )

        return len(deletion_list)


    def list_model_names_prefix(self, prefix, time_order):
        result = []
        names = self.list_model_names_filter(prefix, time_order)

        for name in names:
            if name.startswith(prefix):
                result.append(name)

        return result


    def list_model_names_filter(self, string_filter, time_order):
        names = []
        next_token = None

        while True:
            res, next_token = self.retrieve_filtered_models(string_filter, time_order, next_token)
            models = res.get("Models")

            for item in models:
                name = item.get("ModelName")
                names.append(name)

            if not next_token:
                return names


    def list_model_names(self, time_order):
        names = []
        next_token = None

        while True:
            res, next_token = self.retrieve_models(time_order, next_token)
            models = res.get("Models")

            for item in models:
                name = item.get("ModelName")
                names.append(name)

            if not next_token:
                return names


    def retrieve_models(self, time_order, next_token=None):
        next_token2 = None

        if next_token:
            response = self.__client.list_models(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
                NextToken=next_token
            )
        else:
            response = self.__client.list_models(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100
            )

        if "NextToken" in response:
            next_token2 = response.get("NextToken")

        return response, next_token2


    def retrieve_filtered_models(self, filter_string, time_order, next_token=None):
        next_token2 = None

        if next_token:
            response = self.__client.list_models(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
                NameContains=filter_string,
                NextToken=next_token
            )
        else:
            response = self.__client.list_models(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
                NameContains=filter_string
            )

        if "NextToken" in response:
            next_token2 = response.get("NextToken")

        return response, next_token2


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SagemakerModelManager:{client:%s}" % self.__client

