"""
Created on 2 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DEVICE    TYPE      STATE      CONNECTION
eth0      ethernet  connected  Ethernet eth0
cdc-wdm0  gsm       connected  giffgaff
sit0      iptunnel  unmanaged  --
lo        loopback  unmanaged  --

example JSON:
{"eth0": {"kind": "ethernet", "state": "connected", "connection": "Ethernet eth0"},
"cdc-wdm0": {"kind": "gsm", "state": "connected", "connection": "giffgaff"}}
"""

import re

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class Network(JSONable):
    """
    classdocs
    """

    __EXCLUDED_STATES = ('state', 'unmanaged')

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, device=None):
        if not jdict:
            return None

        kind = jdict.get('kind')
        state = jdict.get('state')
        connection = jdict.get('conn')

        return cls(device, kind, state, connection)


    @classmethod
    def construct_from_nmcli(cls, line):
        match = re.match(r'(\S+)\s+(\S+)\s+(\S+)\s+(\S.+)', line)

        if not match:
            return None

        state = match.groups()[2]

        if state.lower() in cls.__EXCLUDED_STATES:
            return None

        device = match.groups()[0]
        kind = match.groups()[1]

        reported_connection = match.groups()[3].strip()
        connection = None if reported_connection == '--' else reported_connection

        return cls(device, kind, state, connection)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, kind, state, connection):
        """
        Constructor
        """
        self.__device = device                      # string
        self.__kind = kind                          # string
        self.__state = state                        # string
        self.__connection = connection              # string


    def __eq__(self, other):
        try:
            return self.device == other.device and self.kind == other.kind and \
                   self.state == other.state and self.connection == other.connection

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device(self):
        return self.__device


    @property
    def kind(self):
        return self.__kind


    @property
    def state(self):
        return self.__state


    @property
    def connection(self):
        return self.__connection


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['kind'] = self.kind
        jdict['state'] = self.state

        if self.connection:
            jdict['conn'] = self.connection

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Network:{device:%s, kind:%s, state:%s, connection:%s}" %  \
               (self.device, self.kind, self.state, self.connection)


# --------------------------------------------------------------------------------------------------------------------

class Networks(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        networks = OrderedDict()

        for device, network_jdict in jdict.items():
            networks[device] = Network.construct_from_jdict(network_jdict, device=device)

        return cls(networks)


    @classmethod
    def construct_from_nmcli(cls, lines):
        networks = OrderedDict()

        for line in lines:
            network = Network.construct_from_nmcli(line)

            if network:
                networks[network.device] = network

        return cls(networks)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, networks):
        """
        Constructor
        """
        self.__networks = networks                  # OrderedDict of device: Network


    def __len__(self):
        return len(self.networks)


    def __eq__(self, other):
        try:
            if len(self) != len(other):
                return False

            for device in self.__networks.keys():
                if self.__networks[device] != other.__networks[device]:
                    return False

            return True

        except (KeyError, TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def networks(self):
        return self.__networks


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.networks


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Networks:{networks:%s}" %  Str.collection(self.networks)
