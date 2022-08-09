"""
Created on 08 Mar 2021
Modified on 21 Sep 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://stackoverflow.com/questions/36780856/complete-scan-of-dynamodb-with-boto3

https://github.com/boto/botocore/issues/1688

A single manager for all required dynamoDB related functions.

"""
# --------------------------------------------------------------------------------------------------------------------
from boto3.dynamodb.conditions import Key, Attr


# --------------------------------------------------------------------------------------------------------------------


class DynamoManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, dynamo_client, dynamo_resource):
        self.__dynamo_client = dynamo_client
        self.__dynamo_resource = dynamo_resource

    # ----------------------------------------------------------------------------------------------------------------
    # SINGLE ITEMS
    # ----------------------------------------------------------------------------------------------------------------
    def get(self, table_name, pk, pk_val, sk=None, sk_val=None):
        # get specific item
        table = self.__dynamo_resource.Table(table_name)
        if sk and sk_val:
            key = {pk: pk_val, sk: sk_val}
        elif pk and pk_val:
            key = {pk: pk_val}
        else:
            return None

        response = table.get_item(Key=key)
        return response['Item'] if 'Item' in response else None

    def exists(self, table_name, pk, pk_val, sk=None, sk_val=None):
        table = self.__dynamo_resource.Table(table_name)
        if sk is None and sk_val is None:
            response = table.query(
                KeyConditionExpression=Key(pk).eq(pk_val)
            )
        else:
            response = table.query(
                KeyConditionExpression=Key(pk).eq(pk_val) & Key(sk).eq(sk_val)
            )
        return response['Items'] if 'Items' in response else None

    def add(self, table_name, item):
        table = self.__dynamo_resource.Table(table_name)

        response = table.put_item(
            Item=item
        )

        return response

    def add_simple(self, table_name, pk, pk_val, sk=None, sk_val=None):
        table = self.__dynamo_resource.Table(table_name)
        if sk and sk_val:
            item = {pk: pk_val, sk: sk_val}
        elif pk and pk_val and not sk and sk_val:
            item = {pk: pk_val}
        else:
            return None

        response = table.put_item(
            Item=item
        )

        return response

    def delete(self, table_name, pk, pk_val, sk=None, sk_val=None):
        table = self.__dynamo_resource.Table(table_name)
        if pk and pk_val and sk and sk_val:
            item = {pk: pk_val, sk: sk_val}
        elif pk and pk_val and not sk and not sk_val:
            item = {pk: pk_val}
        else:
            return None

        response = table.delete_item(
            Key=item
        )

        return response

    def delete_item(self, table_name, item):
        table = self.__dynamo_resource.Table(table_name)

        response = table.delete_item(
            Key=item
        )

        return response

    def update_item(self, table_name, pk, update_expression, eav):
        table = self.__dynamo_resource.Table(table_name)
        response = table.update_item(
            Key=pk,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=eav,
            ReturnValues="UPDATED_NEW"
        )

        return response

    # ----------------------------------------------------------------------------------------------------------------
    # MAIN FUNCTIONALITY
    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def build_query(table_name, pk=None, pk_val=None, sk=None, sk_val=None, keys_only=False, exact=False,
                    limit=None, fosk=False):

        kwargs = {}

        if not table_name:
            return kwargs

        # retrieve all - retrieve all batched - retrieve all keys only
        if pk_val is None and sk is None and sk_val is None:
            if keys_only:
                kwargs['ProjectionExpression'] = '#pk'
                kwargs['ExpressionAttributeNames'] = {'#pk': pk}
            if limit:
                kwargs['Limit'] = limit
            return kwargs

        # retrieve filtered on pk - retrieve filtered on pk keys only - retrieve filtered on pk batched
        if pk and pk_val and sk is None and sk_val is None and not fosk:
            if exact:
                kwargs['FilterExpression'] = (Attr(pk).eq(pk_val))
            else:
                kwargs['FilterExpression'] = (Attr(pk).contains(pk_val))
            if limit:
                kwargs['Limit'] = limit
            if keys_only:
                kwargs['ProjectionExpression'] = '#pk'
                kwargs['ExpressionAttributeNames'] = {'#pk': pk}

            return kwargs

        # retrieve double filtered - retrieve double filtered keys only - retrieve double filtered batched
        # basically the same as a get but can also be used with batch, exact and reserved keys
        if pk and pk_val and sk and sk_val and not fosk:
            if exact:
                kwargs['FilterExpression'] = Attr(pk).eq(pk_val) & Attr(sk).eq(sk_val)
            else:
                kwargs['FilterExpression'] = Attr(pk).contains(pk_val) & Attr(sk).contains(sk_val)
            if limit:
                kwargs['Limit'] = limit
            if keys_only:
                kwargs['ProjectionExpression'] = '#pk'
                kwargs['ExpressionAttributeNames'] = {'#pk': pk}

            return kwargs

        # Filter on second key - filter on second key keys only - filter on second key batched
        if pk and sk and sk_val and fosk:
            kwargs['ProjectionExpression'] = pk
            if exact:
                kwargs['FilterExpression'] = Attr(sk).eq(sk_val)
            else:
                kwargs['FilterExpression'] = Attr(sk).contains(sk_val)
            if limit:
                kwargs['Limit'] = limit
            if keys_only:
                kwargs['ProjectionExpression'] = '#pk'
                kwargs['ExpressionAttributeNames'] = {'#pk': pk}

            return kwargs

    def do_query(self, table_name, query, limited=False):
        table = self.__dynamo_resource.Table(table_name)
        to_return = []
        q = table.scan(**query)
        to_return.extend(q['Items'])
        if not limited:
            while 'LastEvaluatedKey' in q:
                query['ExclusiveStartKey'] = q['LastEvaluatedKey']
                q = table.scan(**query)
                to_return.extend(q['Items'])
        return to_return

    def do_query_batched(self, table_name, query, exclusive_start_key=None):
        last_evaluated_key = None
        table = self.__dynamo_resource.Table(table_name)
        to_return = []
        if exclusive_start_key:
            query['ExclusiveStartKey'] = exclusive_start_key
        q = table.scan(**query)
        to_return.extend(q['Items'])
        if 'LastEvaluatedKey' in q:
            last_evaluated_key = q['LastEvaluatedKey']

        return to_return, last_evaluated_key

    # ----------------------------------------------------------------------------------------------------------------
    # UTILITIES
    # ----------------------------------------------------------------------------------------------------------------

    def describe_table(self, table_name):
        response = self.__dynamo_client.describe_table(
            TableName=table_name
        )

        return response

    def return_key_schema(self, table_name):
        table = self.__dynamo_resource.Table(table_name)
        return table.key_schema

    # ----------------------------------------------------------------------------------------------------------------
    # BATCH FUNCTIONS
    # ----------------------------------------------------------------------------------------------------------------

    def batch_delete(self, table_name, items):
        table = self.__dynamo_resource.Table(table_name)
        with table.batch_writer() as batch:
            for item in items:
                batch.delete_item(item)

    def batch_write(self, table_name, items):
        table = self.__dynamo_resource.Table(table_name)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

# --------------------------------------------------------------------------------------------------------------------
