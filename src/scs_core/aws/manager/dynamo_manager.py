"""
Created on 08 Mar 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://stackoverflow.com/questions/36780856/complete-scan-of-dynamodb-with-boto3
"""

import logging

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


# --------------------------------------------------------------------------------------------------------------------

class DynamoManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, dynamo_client, dynamo_resource):
        self.__dynamo_client = dynamo_client
        self.__dynamo_resource = dynamo_resource
        self.__logger = logging.getLogger()


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


    def retrieve_all(self, table_name):
        datum = []
        table = self.__dynamo_resource.Table(table_name)
        response = table.scan()

        if "Items" not in response:
            return None

        data = response['Items']
        print(data)

        try:
            lek = data["LastEvaluatedKey"]
        except KeyError:
            return data["Items"]

        while lek is not None:
            lek, data = self.scan(table_name, lek)
            datum.append(data)

        return datum


    def scan(self, table_name, lek):
        response = self.__dynamo_client.scan(
            TableName=table_name,
            ExclusiveStartKey=lek
        )

        data = response.json()

        if "Items" not in data:
            return None, None

        try:
            lek = data["LastEvaluatedKey"]
        except KeyError:
            return None, data["Items"]

        return lek, data["Items"]

    def includes(self, table_name, scan_key, scan_value, lek):

        table = self.__dynamo_resource.Table(table_name)
        table.scan(
            FilterExpression=Attr(scan_key).contains(scan_value)
        )
        response = self.__dynamo_client.scan(
            TableName=table_name,
            ExclusiveStartKey=lek
        )

        data = response.json()

        if "Items" not in data:
            return None, None

        try:
            lek = data["LastEvaluatedKey"]
        except KeyError:
            return None, data["Items"]

        return lek, data["Items"]
