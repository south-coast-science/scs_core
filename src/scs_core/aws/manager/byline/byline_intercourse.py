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

        return cls(items, next_url=next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items, next_url=None):
        """
        Constructor
        """
        self.__items = items                                # list of Byline
        self.__next_url = next_url                          # URL string


    def __len__(self):
        return len(self.items)


    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, _):
        return parse_qs(urlparse(self.next_url).query)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.items is not None:
            jdict['Items'] = self.items
            jdict['itemCount'] = len(self.items)

        if self.next_url is not None:
            jdict['next'] = self.next_url

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def items(self):
        return self.__items


    @property
    def next_url(self):
        return self.__next_url


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BylineFinderResponse:{items:%s, next_url:%s}" %  (Str.collection(self.items), self.next_url)
