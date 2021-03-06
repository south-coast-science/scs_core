"""
Created on 08 Mar 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://stackoverflow.com/questions/36780856/complete-scan-of-dynamodb-with-boto3
"""

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from scs_core.sys.logging import Logging


# TODO: where does sorting happen?

# --------------------------------------------------------------------------------------------------------------------

class DynamoManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, dynamo_client, dynamo_resource):
        self.__dynamo_client = dynamo_client
        self.__dynamo_resource = dynamo_resource

        self.__logger = Logging.getLogger()

    # ----------------------------------------------------------------------------------------------------------------

    def get(self, table_name, primary_key):
        # get specific item
        table = self.__dynamo_resource.Table(table_name)
        try:
            response = table.get_item(Key=primary_key)
        except ClientError as e:
            self.__logger.error(e.response['Error']['Message'])
        else:
            return response['Item'] if 'Item' in response else None

    def exists(self, table_name, primary_key_name, primary_key):
        table = self.__dynamo_resource.Table(table_name)
        try:
            response = table.query(
                KeyConditionExpression=Key(primary_key_name).eq(primary_key)
            )
        except ClientError as e:
            self.__logger.error(e.response['Error']['Message'])
        else:
            return response['Items'] if 'Items' in response else None

    def add(self, table_name, item):
        table = self.__dynamo_resource.Table(table_name)

        response = table.put_item(
            Item=item
        )
        self.__logger.info(response)

    def delete(self, table_name, item):
        table = self.__dynamo_resource.Table(table_name)
        response = None

        try:
            response = table.delete_item(
                Key=item
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                self.__logger.error(e.response['Error']['Message'])
            else:
                raise

        return response

    def retrieve_all(self, table_name, lek=None):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)

        if lek:
            response = table.scan(LastEvaluatedKey=lek)
        else:
            response = table.scan()

        if "Items" not in response:
            return None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        try:
            lek = response["LastEvaluatedKey"]
        except KeyError:
            lek = None

        while lek is not None:
            data = self.retrieve_all(table_name, lek)
            data_dict += data

        return data_dict

    def retrieve_filtered(self, table_name, filter_key, filter_value, lek=None):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)
        if lek:
            response = table.scan(
                FilterExpression=Attr(filter_key).contains(filter_value),
                LastEvaluatedKey=lek
            )
        else:
            response = table.scan(
                FilterExpression=Attr(filter_key).contains(filter_value)
            )

        if "Items" not in response:
            return None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        try:
            lek = response["LastEvaluatedKey"]
        except KeyError:
            lek = None

        while lek is not None:
            data = self.retrieve_filtered(table_name, filter_key, filter_value, lek)
            data_dict += data

        return data_dict

    def retrieve_all_pk(self, table_name, pk, lek=None):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)

        if lek:
            response = table.scan(
                ProjectionExpression=pk,
                LastEvaluatedKey=lek
            )
        else:
            response = table.scan(
                ProjectionExpression=pk
            )

        if "Items" not in response:
            return None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        try:
            lek = response["LastEvaluatedKey"]
        except KeyError:
            lek = None

        while lek is not None:
            data = self.retrieve_all_pk(table_name, pk, lek)
            data_dict += data

        return data_dict

    def retrieve_filtered_pk(self, table_name, pk, tag_filter, lek=None):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)

        if lek:
            response = table.scan(
                FilterExpression=Attr(pk).contains(tag_filter),
                ProjectionExpression=pk,
                LastEvaluatedKey=lek
            )
        else:
            response = table.scan(
                FilterExpression=Attr(pk).contains(tag_filter),
                ProjectionExpression=pk
            )

        if "Items" not in response:
            return None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        try:
            lek = response["LastEvaluatedKey"]
        except KeyError:
            lek = None

        while lek is not None:
            data = self.retrieve_all_pk(table_name, pk, lek)
            data_dict += data

        return data_dict

    def retrieve_double_filtered(self, table_name, first_key, first_value, second_key, second_value, lek=None):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)
        if lek:
            response = table.scan(
                FilterExpression=Attr(first_key).contains(first_value) & Attr(second_key).contains(second_value),
                LastEvaluatedKey=lek
            )
        else:
            response = table.scan(
                FilterExpression=Attr(first_key).contains(first_value) & Attr(second_key).contains(second_value)
            )

        if "Items" not in response:
            return None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        try:
            lek = response["LastEvaluatedKey"]
        except KeyError:
            lek = None

        while lek is not None:
            data = self.retrieve_filtered(table_name, first_key, first_value, lek)
            data_dict += data

        return data_dict

    def retrieve_double_filtered_pk(self, table_name, first_key, first_value, second_key, second_value, lek=None):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)
        if lek:
            response = table.scan(
                FilterExpression=Attr(first_key).contains(first_value) & Attr(second_key).contains(second_value),
                ProjectionExpression=first_key,
                LastEvaluatedKey=lek
            )
        else:
            response = table.scan(
                FilterExpression=Attr(first_key).contains(first_value) & Attr(second_key).contains(second_value),
                ProjectionExpression=first_key
            )

        if "Items" not in response:
            return None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        try:
            lek = response["LastEvaluatedKey"]
        except KeyError:
            lek = None

        while lek is not None:
            data = self.retrieve_filtered(table_name, first_key, first_value, lek)
            data_dict += data

        return data_dict

