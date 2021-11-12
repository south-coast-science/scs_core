"""
Created on 14 Oct 2021

@author: Jade Page (jade.page@southcoastscience.com)

A class holding RDS functionality

https://johnkeefe.net/amazon-aurora-mysql-plus-python

https://stackoverflow.com/questions/59742083/passing-in-iam-credentials-when-using-the-aurora-serverless-data-api

https://github.com/cal-poly-dxhub/covid-dashboard/blob/1d4d3f9abe82e84c22d294642e733b5bfffb2780/lambda/utility.py

"""
# --------------------------------------------------------------------------------------------------------------------
import ast
import json
import logging

# --------------------------------------------------------------------------------------------------------------------



class RDSManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rds_client, secret_arn, database, resource_arn):
        self.__rds_client = rds_client  # session.client('rds')
        self.__secretArn = secret_arn
        self.__database = database
        self.__resourceArn = resource_arn

    # ----------------------------------------------------------------------------------------------------------------

    def execute_query_raw(self, q):
        res = self.__rds_client.execute_statement(
            secretArn=self.__secretArn,
            database=self.__database,
            resourceArn=self.__resourceArn,
            sql=q
        )
        logging.info(res)
        return res

    def execute_query_mapped(self, q):
        res = self.__rds_client.execute_statement(
            includeResultMetadata=True,
            secretArn=self.__secretArn,
            database=self.__database,
            resourceArn=self.__resourceArn,
            sql=q
        )
        return self.generate_map_from_response(res)

    @staticmethod
    def generate_map_from_response(response):
        response_set = []
        obj = {}
        for record in response['records']:
            for i in range(len(record)):
                obj[response['columnMetadata'][i]['label']] = list(record[i].values())[0]
            response_set.append(obj.copy())
        return response_set

# --------------------------------------------------------------------------------------------------------------------


class RDSLambdaManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lambda_client):
        self.__lambda_client = lambda_client


    def get_raw_response(self, q, user):
        event = {
            "query": q,
            "username": user
        }
        payload = json.dumps(event).encode('utf-8')

        res = self.__lambda_client.invoke(
            FunctionName="arn:aws:lambda:us-west-2:696437392763:function:RDSExecutor",
            InvocationType='RequestResponse',
            Payload=payload
        )

        return res

    def get_records(self, q, user):
        event = {
            "query": q,
            "username": user
        }
        payload = json.dumps(event).encode('utf-8')

        res = self.__lambda_client.invoke(
            FunctionName="arn:aws:lambda:us-west-2:696437392763:function:RDSExecutor",
            InvocationType='RequestResponse',
            Payload=payload
        )

        raw = res['Payload'].read().decode('utf-8')
        jdict = json.loads(ast.literal_eval(raw))
        logging.info(jdict)
        if type(jdict) is str:
            return None
        return jdict

    def do_query(self, q, user):
        event = {
            "query": q,
            "username": user
        }
        payload = json.dumps(event).encode('utf-8')

        self.__lambda_client.invoke(
            FunctionName="arn:aws:lambda:us-west-2:696437392763:function:RDSExecutor",
            InvocationType='RequestResponse',
            Payload=payload
        )


    """
    TODO: Could this be made more efficient, maybe by getting one row with raw metadata to do the 
    mapping and the rest without? Is there any guarantee all calls are extracted in the same order???
    """

    @staticmethod
    def do_mapping(response):
        response_set = []
        obj = {}
        for record in response['records']:
            for i in range(len(record)):
                obj[response['columnMetadata'][i]['label']] = list(record[i].values())[0]
            response_set.append(obj.copy())
        return response_set
