"""
Created on 08 Mar 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html#GettingStarted.Python.03.02


"""

# ----------------------------------------------------------------------------------------------------------------
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import logging


class DynamoManager(object):

    def __init__(self, dynamo_client, dynamo_resource):
        self.__dynamo_client = dynamo_client
        self.__dynamo_resource = dynamo_resource
        self.__logger = logging.getLogger()

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
