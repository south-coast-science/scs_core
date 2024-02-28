"""
Created on 15 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

aws lambda add-permission --function-name "arn:aws:lambda:us-west-2:696437392763:function:CognitoLogin:Production" \
--source-arn "arn:aws:execute-api:us-west-2:696437392763:lnh2y9ip75/*/*/CognitoLogin/user" \
--principal apigateway.amazonaws.com --statement-id 8ad4f802-a2c0-4e30-948c-416477a6f8c4 \
--action lambda:InvokeFunction

https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-custom-domains.html
https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-custom-domains-prerequisites.html

https://docs.aws.amazon.com/apigateway/latest/developerguide/stage-variables.html
https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-set-stage-variables-aws-console.html
https://docs.aws.amazon.com/apigateway/latest/developerguide/aws-api-gateway-stage-variables-reference.html

Route 53 is a bad idea
"""

import socket


# --------------------------------------------------------------------------------------------------------------------

class AWS(object):
    """
    classdocs
    """

    __USE_RAW_URLS = False

    __API_DOMAIN_NAME =     'api.southcoastscience.com'
    __REGION =              'us-west-2'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def endpoint_url(cls, production_path, raw):
        return raw if cls.__USE_RAW_URLS else 'https://' + cls.__API_DOMAIN_NAME + '/' + production_path


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def region(cls):
        return cls.__REGION


    @classmethod
    def group_name(cls):
        host_name = socket.gethostname()
        return host_name + "-group"


    @classmethod
    def core_name(cls):
        host_name = socket.gethostname()
        return host_name + "-core"

