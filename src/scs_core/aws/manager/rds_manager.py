"""
Created on 14 Oct 2021

@author: Jade Page (jade.page@southcoastscience.com)

A class holding RDS functionality

https://johnkeefe.net/amazon-aurora-mysql-plus-python

https://stackoverflow.com/questions/59742083/passing-in-iam-credentials-when-using-the-aurora-serverless-data-api

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

    def execute_query(self, q):
        res = self.__rds_client.execute_statement(
            secretArn=self.__secretArn,
            database=self.__database,
            resourceArn=self.__resourceArn,
            sql=q
        )
        logging.info(res)
        return res

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
            "q": q,
            "user": user
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
        return jdict["records"]

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
