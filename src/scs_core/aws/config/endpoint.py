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

Route 53 is unnecessary
"""

from abc import ABC, abstractmethod

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(ABC):
    """
    classdocs
    """

    USE_RAW_URLS = False
    DEFAULT_AUTH = '@southcoastscience.com'

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
    def url(cls, *path_extensions):
        return cls.configuration().selected_url(*path_extensions)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, production_path, raw_url):
        self.__production_path = production_path
        self.__raw_url = raw_url


    # ----------------------------------------------------------------------------------------------------------------

    def selected_url(self, *path_extensions):
        url = self.raw_url if self.USE_RAW_URLS else self.production_url
        extended_url = '/'.join([url] + [str(extension) for extension in path_extensions])

        Logging.getLogger().info('API: %s' % extended_url)

        return extended_url


    @property
    @abstractmethod
    def production_url(self):
        pass


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


# --------------------------------------------------------------------------------------------------------------------

class APIEndpoint(Endpoint, ABC):
    """
    classdocs
    """

    API_DOMAIN_NAME =   'api.southcoastscience.com'

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def production_url(self):
        return 'https://' + self.API_DOMAIN_NAME + '/' + self.production_path


# --------------------------------------------------------------------------------------------------------------------

class AWSEndpoint(Endpoint, ABC):
    """
    classdocs
    """

    API_DOMAIN_NAME =   'aws.southcoastscience.com'

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def production_url(self):
        return 'https://' + self.API_DOMAIN_NAME + '/' + self.production_path
