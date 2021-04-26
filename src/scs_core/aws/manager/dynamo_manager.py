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
        datum = []
        table = self.__dynamo_resource.Table(table_name)

        if lek:
            response = table.scan(LastEvaluatedKey=lek)
        else:
            response = table.scan()

        if "Items" not in response:
            return None

        data = response['Items']
        for item in data:
            datum.append(item)

        try:
            lek = response["LastEvaluatedKey"]
        except KeyError:
            lek = None

        while lek is not None:
            data = self.retrieve_all(table_name, lek)
            datum.append(data)

        return datum

    def retrieve_selective(self, table_name, scan_key, scan_value, lek=None):
        datum = []
        table = self.__dynamo_resource.Table(table_name)
        if lek:
            response = table.scan(
                FilterExpression=Attr(scan_key).contains(scan_value),
                LastEvaluatedKey=lek
            )
        else:
            response = table.scan(
                FilterExpression=Attr(scan_key).contains(scan_value)
            )

        if "Items" not in response:
            return None

        data = response['Items']
        for item in data:
            datum.append(item)

        try:
            lek = response["LastEvaluatedKey"]
        except KeyError:
            lek = None

        while lek is not None:
            data = self.retrieve_selective(table_name, scan_key, scan_value, lek)
            datum.append(data)

        return datum

    def retrieve_all_pk(self, table_name, pk, lek=None):
        datum = []
        table = self.__dynamo_resource.Table(table_name)

        if lek:
            response = table.scan(
                AttributesToGet=["tag"],
                LastEvaluatedKey=lek
            )
        else:
            response = table.scan(
                AttributesToGet=["tag"]
            )

        if "Items" not in response:
            return None

        data = response['Items']
        for item in data:
            datum.append(item)

        try:
            lek = response["LastEvaluatedKey"]
        except KeyError:
            lek = None

        while lek is not None:
            data = self.retrieve_all_pk(table_name, pk, lek)
            datum.append(data)

        return datum
