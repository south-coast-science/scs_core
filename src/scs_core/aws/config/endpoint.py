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

EndpointAccess should be initialised in scs_host.sys.__init__

example document:
{"use-default-urls": false, "report-urls": true}
"""

from abc import ABC, abstractmethod
from collections import OrderedDict

from scs_core.data.json import PersistentJSONable
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class EndpointAccess(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "endpoint_access.json"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    __CONFIG = None

    @classmethod
    def init(cls, manager):
        cls.__CONFIG = cls.load(manager, skeleton=True)


    @classmethod
    def config(cls):
        return cls.default() if cls.__CONFIG is None else cls.__CONFIG


    @classmethod
    def default(cls):
        return cls(False, False)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls.default() if skeleton else None

        use_default_urls = jdict.get('use-default-urls', False)
        report_urls = jdict.get('report-urls', False)

        return cls(use_default_urls, report_urls)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, use_default_urls, report_urls):
        """
        Constructor
        """
        super().__init__()

        self.__use_default_urls = bool(use_default_urls)            # bool
        self.__report_urls = bool(report_urls)                      # bool


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['use-default-urls'] = self.use_default_urls
        jdict['report-urls'] = self.report_urls

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def use_default_urls(self):
        return self.__use_default_urls


    @property
    def report_urls(self):
        return self.__report_urls


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "EndpointAccess:{use_default_urls:%s, report_urls:%s}" %  (self.use_default_urls, self.report_urls)


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(ABC):
    """
    classdocs
    """

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
        self.__production_path = production_path                # string
        self.__raw_url = raw_url                                # string

        self.__access = EndpointAccess.config()


    # ----------------------------------------------------------------------------------------------------------------

    def selected_url(self, *path_extensions):
        url = self.raw_url if self.access.use_default_urls else self.production_url
        extended_url = '/'.join([url] + [str(extension) for extension in path_extensions])

        if self.access.report_urls:
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


    @property
    def access(self):
        return self.__access


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (self.__class__.__name__ + ":{production_path:%s, raw_url:%s, access:%s}" %
                (self.production_path, self.raw_url, self.access))


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
