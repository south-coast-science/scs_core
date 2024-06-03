"""
Created on 2 Oct 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Equivalent to cURLs:
curl "https://aws.southcoastscience.com/device-topics?topic=south-coast-science-dev/alphasense/loc/303/gases"
curl "https://aws.southcoastscience.com/device-topics?device=scs-bgx-303"
"""

from collections import OrderedDict
from urllib.parse import parse_qs, urlparse

from scs_core.aws.client.api_intercourse import APIResponse
from scs_core.aws.manager.byline.byline import Byline

from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class BylineFinderResponse(APIResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        items = []
        if jdict.get('Items'):
            for item_jdict in jdict.get('Items'):
                item = Byline.construct_from_jdict(item_jdict)
                items.append(item)

        next_url = jdict.get('next')

        return cls(items, next_request=next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items, next_request=None):
        """
        Constructor
        """
        self.__items = items                                # list of Byline
        self.__next_request = next_request                  # dict (lambda-to-lambda) or URL string (API gateway)


    def __len__(self):
        return len(self.items)


    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, _):
        return parse_qs(urlparse(self.next_request).query)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        if self.items is not None:
            jdict['Items'] = self.items
            jdict['itemCount'] = len(self.items)

        if self.next_request is not None:
            jdict['next'] = self.next_request

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def items(self):
        return self.__items


    @property
    def next_request(self):
        return self.__next_request


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BylineFinderResponse:{items:%s, next_request:%s}" %  (Str.collection(self.items), self.next_request)
