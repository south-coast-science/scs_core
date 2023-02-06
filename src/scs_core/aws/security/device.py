"""
Created on 2 Feb 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
"""

from collections import OrderedDict

from scs_core.aws.security.cognito_device import CognitoDeviceIdentity

from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class Device(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, identity: CognitoDeviceIdentity, deployments):
        """
        Constructor
        """
        self.__identity = identity                          # CognitoDeviceIdentity
        self.__deployments = deployments                    # array of OrganisationDevice


    def __lt__(self, other):
        return self.identity < other.identity


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['identity'] = self.identity
        jdict['deployments'] = self.deployments

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def identity(self):
        return self.__identity


    @property
    def deployments(self):
        return self.__deployments


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Device:{identity:%s, deployments:%s}" % \
               (self.identity, Str.collection(self.deployments))
