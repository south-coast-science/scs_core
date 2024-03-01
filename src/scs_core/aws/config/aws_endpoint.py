"""
Created on 1 Mar 2024

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

Route 53 is unecessary
"""

from abc import ABC, abstractmethod

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class AWSEndpoint(ABC):
    """
    classdocs
    """

    USE_RAW_URLS =      False
    API_DOMAIN_NAME =   'api.southcoastscience.com'
    STD_AUTH =          '@southcoastscience.com'


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def header(cls, accept='text/json', auth=None, token=None):
        header = {"Content-type": "application/x-www-form-urlencoded", "Accept": accept}

        if auth is not None:
            header["Authorization"] = auth

        if token is not None:
            header["Token"] = token

        return header


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def configuration(cls):
        pass

    @classmethod
    def url(cls):
        return cls.configuration().selected_url()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, production_path, raw_url):
        self.__production_path = production_path
        self.__raw_url = raw_url


    # ----------------------------------------------------------------------------------------------------------------

    def selected_url(self):
        url = self.raw_url if self.USE_RAW_URLS else 'https://' + self.API_DOMAIN_NAME + '/' + self.production_path
        Logging.getLogger().info('endpoint: %s' % url)

        return url


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def production_path(self):
        return self.__production_path


    @property
    def raw_url(self):
        return self.__raw_url


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{production_path:%s, raw_url:%s}" % (self.production_path, self.raw_url)
