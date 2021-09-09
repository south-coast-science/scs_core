"""
Created on 08 Mar 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://stackoverflow.com/questions/36780856/complete-scan-of-dynamodb-with-boto3
"""
import logging

from boto3.dynamodb.conditions import Key, Attr

from botocore.exceptions import ClientError

from scs_core.sys.logging import Logging


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
            response = table.scan(ExclusiveStartKey=lek)
        else:
            response = table.scan()

        if "Items" not in response:
            return None, None

        if response['ScannedCount'] == 0:
            return None, None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        if "LastEvaluatedKey" not in response:
            return data_dict, None
        else:
            lek = response["LastEvaluatedKey"]

        while lek is not None:
            data, lek = self.retrieve_all(table_name, lek)
            try:
                data_dict += data
            except TypeError:
                lek = None

        return data_dict, lek


    def retrieve_filtered(self, table_name, filter_key, filter_value, exact=False, lek=None):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)

        if exact is True:
            self.__logger.info("Doing exact")
            if lek:
                response = table.scan(
                    FilterExpression=Attr(filter_key).eq(filter_value),
                    ExclusiveStartKey=lek
                )
            else:
                response = table.scan(
                    FilterExpression=Attr(filter_key).eq(filter_value)
                )
        else:
            if lek:
                response = table.scan(
                    FilterExpression=Attr(filter_key).contains(filter_value),
                    ExclusiveStartKey=lek
                )
            else:
                response = table.scan(
                    FilterExpression=Attr(filter_key).contains(filter_value)
                )

        if "Items" not in response:
            return None, None

        if response['ScannedCount'] == 0:
            return None, None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        if "LastEvaluatedKey" not in response:
            return data_dict, None
        else:
            lek = response["LastEvaluatedKey"]

        while lek is not None:
            logging.info("Continuing with LEK %s" % lek)
            data, lek = self.retrieve_filtered(table_name, filter_key, filter_value, exact, lek)
            try:
                data_dict += data
            except TypeError:
                lek = None

        return data_dict, lek


    def retrieve_all_pk(self, table_name, pk, lek=None):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)

        if lek:
            response = table.scan(
                ProjectionExpression='#pk',
                ExpressionAttributeNames={'#pk': pk},
                ExclusiveStartKey=lek
            )
        else:
            response = table.scan(
                ProjectionExpression=pk
            )

        if "Items" not in response:
            return None, None

        if response['ScannedCount'] == 0:
            return None, None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        if "LastEvaluatedKey" not in response:
            return data_dict, None
        else:
            lek = response["LastEvaluatedKey"]

        while lek is not None:
            data, lek = self.retrieve_all_pk(table_name, pk, lek)
            try:
                data_dict += data
            except TypeError:
                lek = None

        return data_dict, lek


    def retrieve_filtered_pk(self, table_name, pk, tag_filter, exact=False, lek=None):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)

        print(table_name, pk, exact, tag_filter)

        if exact is True:
            self.__logger.info("Doing exact")
            if lek:
                response = table.scan(
                    FilterExpression=Attr(pk).eq(tag_filter),
                    ProjectionExpression='#pk',
                    ExpressionAttributeNames={'#pk': pk},
                    ExclusiveStartKey=lek
                )
            else:
                response = table.scan(
                    FilterExpression=Attr(pk).eq(tag_filter),
                    ProjectionExpression='#pk',
                    ExpressionAttributeNames={'#pk': pk}
                )
        else:
            if lek:
                response = table.scan(
                    FilterExpression=Attr(pk).contains(tag_filter),
                    ProjectionExpression='#pk',
                    ExpressionAttributeNames={'#pk': pk},
                    ExclusiveStartKey=lek
                )
            else:
                response = table.scan(
                    FilterExpression=Attr(pk).contains(tag_filter),
                    ProjectionExpression='#pk',
                    ExpressionAttributeNames={'#pk': pk}
                )

        if "Items" not in response:
            return None, None

        if response['ScannedCount'] == 0:
            return None, None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        if "LastEvaluatedKey" not in response:
            return data_dict, None
        else:
            lek = response["LastEvaluatedKey"]

        while lek is not None:
            data, lek = self.retrieve_filtered_pk(table_name, pk, tag_filter, exact, lek)
            try:
                data_dict += data
            except TypeError:
                lek = None

        return data_dict, lek


    def retrieve_double_filtered(self, table_name, first_key, first_value, second_key, second_value, exact=False,
                                 lek=None):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)

        if exact is True:
            self.__logger.info("Doing exact double filtered")
            if lek:
                response = table.scan(
                    FilterExpression=Attr(first_key).eq(first_value) & Attr(second_key).eq(second_value),
                    ExclusiveStartKey=lek
                )
            else:
                response = table.scan(
                    FilterExpression=Attr(first_key).eq(first_value) & Attr(second_key).eq(second_value)
                )
        else:
            if lek:
                response = table.scan(
                    FilterExpression=Attr(first_key).contains(first_value) & Attr(second_key).contains(second_value),
                    ExclusiveStartKey=lek
                )
            else:
                response = table.scan(
                    FilterExpression=Attr(first_key).contains(first_value) & Attr(second_key).contains(second_value)
                )

        if "Items" not in response:
            return None, None

        if response['ScannedCount'] == 0:
            return None, None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        if "LastEvaluatedKey" not in response:
            return data_dict, None
        else:
            lek = response["LastEvaluatedKey"]

        while lek is not None:
            data, lek = self.retrieve_double_filtered(table_name, first_key, first_value, second_key, second_value,
                                                      exact, lek)
            try:
                data_dict += data
            except TypeError:
                lek = None

        return data_dict, lek


    def retrieve_double_filtered_pk(self, table_name, first_key, first_value, second_key, second_value, lek=None,
                                    exact=False):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)
        if exact is True:
            if lek:
                response = table.scan(
                    FilterExpression=Attr(first_key).eq(first_value) & Attr(second_key).eq(second_value),
                    ProjectionExpression=first_key,
                    ExclusiveStartKey=lek
                )
            else:
                response = table.scan(
                    FilterExpression=Attr(first_key).eq(first_value) & Attr(second_key).eq(second_value),
                    ProjectionExpression=first_key
                )
        else:
            if lek:
                response = table.scan(
                    FilterExpression=Attr(first_key).contains(first_value) & Attr(second_key).contains(second_value),
                    ProjectionExpression=first_key,
                    ExclusiveStartKey=lek
                )
            else:
                response = table.scan(
                    FilterExpression=Attr(first_key).contains(first_value) & Attr(second_key).contains(second_value),
                    ProjectionExpression=first_key
                )

        if "Items" not in response:
            return None, None

        if response['ScannedCount'] == 0:
            return None, None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        if "LastEvaluatedKey" not in response:
            return data_dict, None
        else:
            lek = response["LastEvaluatedKey"]

        while lek is not None:
            data, lek = self.retrieve_double_filtered_pk(table_name, first_key, first_value, second_key, second_value,
                                                         lek)
            try:
                data_dict += data
            except TypeError:
                lek = None

        return data_dict, lek


    def filter_on_second_value(self, table_name, pk, second_key, second_value, lek=None, exact=False):
        data_dict = []
        table = self.__dynamo_resource.Table(table_name)
        if exact:
            if lek:
                response = table.scan(
                    FilterExpression=Attr(second_key).eq(second_value),
                    ProjectionExpression=pk,
                    ExclusiveStartKey=lek
                )
            else:
                response = table.scan(
                    FilterExpression=Attr(second_key).eq(second_value),
                    ProjectionExpression=pk
                )
        else:
            if lek:
                response = table.scan(
                    FilterExpression=Attr(second_key).contains(second_value),
                    ProjectionExpression=pk,
                    ExclusiveStartKey=lek
                )
            else:
                response = table.scan(
                    FilterExpression=Attr(second_key).contains(second_value),
                    ProjectionExpression=pk
                )

        if "Items" not in response:
            return None, None

        if response['ScannedCount'] == 0:
            return None, None

        data = response['Items']
        for item in data:
            data_dict.append(item)

        if "LastEvaluatedKey" not in response:
            return data_dict, None
        else:
            lek = response["LastEvaluatedKey"]

        while lek is not None:
            data, lek = self.filter_on_second_value(table_name, pk, second_key, second_value, lek)
            try:
                data_dict += data
            except TypeError:
                lek = None

        return data_dict, lek


    def update_item(self, table_name, key, update_expression, eav):
        table = self.__dynamo_resource.Table(table_name)
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=eav,
            ReturnValues="UPDATED_NEW"
        )

        return response

    def batch_delete_on_pk(self, table_name, pk, pk_val, sk):
        table = self.__dynamo_resource.Table(table_name)
        to_delete, _lek = self.retrieve_filtered(table_name, pk, pk_val, exact=True)
        item_count = 0
        if to_delete:
            for item in to_delete:
                logging.info("Deleting item %d" % item_count)
                for key, value in list(item.items()):
                    # pop items that aren't key or sort key
                    if key != pk and key != sk:
                        del item[key]

                with table.batch_writer() as batch:
                    res = batch.delete_item(item)
                    logging.info(res)
                    item_count += 1






