"""
Created on 24 Mar 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Subscriber Identity Module (SIM)

sim.dbus-path                             : /org/freedesktop/ModemManager1/SIM/0
sim.properties.imsi                       : 234104886708667
sim.properties.iccid                      : 8944110068256270054
sim.properties.operator-code              : 23410
sim.properties.operator-name              : giffgaff
sim.properties.emergency-numbers.length   : 2
sim.properties.emergency-numbers.value[1] : 999
sim.properties.emergency-numbers.value[2] : 00112

example JSON:
{"imsi": "123", "iccid": "456", "operator-code": "789 012", "operator-name": "giff gaff"}
"""

import re

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SIM(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        imsi = jdict.get('imsi')
        iccid = jdict.get('iccid')
        operator_code = jdict.get('operator-code')
        operator_name = jdict.get('operator-name')

        return cls(imsi, iccid, operator_code, operator_name)


    @classmethod
    def construct_from_mmcli(cls, lines):
        imsi = None
        iccid = None
        operator_code = None
        operator_name = None

        for line in lines:
            match = re.match(r'sim.properties.imsi\s+:\s+([\d]+)', line)
            if match:
                imsi = match.groups()[0]

            match = re.match(r'sim.properties.iccid\s+:\s+([\d]+)', line)
            if match:
                iccid = match.groups()[0]

            match = re.match(r'sim.properties.operator-code\s+:\s+([\d]+)', line)
            if match:
                operator_code = match.groups()[0]

            match = re.match(r'sim.properties.operator-name\s+:\s+(\S.*)', line)
            if match:
                operator_name = match.groups()[0].strip()

        return cls(imsi, iccid, operator_code, operator_name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, imsi, iccid, operator_code, operator_name):
        """
        Constructor
        """
        self.__imsi = imsi                                  # numeric string
        self.__iccid = iccid                                # numeric string
        self.__operator_code = operator_code                # string
        self.__operator_name = operator_name                # string


    def __eq__(self, other):
        try:
            return self.imsi == other.imsi and self.iccid == other.iccid and \
                   self.operator_code == other.operator_code and self.operator_name == other.operator_name

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def imsi(self):
        return self.__imsi


    @property
    def iccid(self):
        return self.__iccid


    @property
    def operator_code(self):
        return self.__operator_code


    @property
    def operator_name(self):
        return self.__operator_name


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['imsi'] = str(self.imsi)
        jdict['iccid'] = str(self.iccid)
        jdict['operator-code'] = self.operator_code
        jdict['operator-name'] = self.operator_name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SIM:{imsi:%s, iccid:%s, operator_code:%s, operator_name:%s}" % \
               (self.imsi, self.iccid, self.operator_code, self.operator_name)


# --------------------------------------------------------------------------------------------------------------------

class ModemList(object):
    """
    modem-list.value[1] : /org/freedesktop/ModemManager1/Modem/0
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_mmcli(cls, lines):
        modems = []

        for line in lines:
            match = re.match(r'modem-list.value\[[\d]+]\s+:\s+([\S]+)', line)
            if match:
                modems.append(match.groups()[0])

        return cls(modems)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, modems):
        """
        Constructor
        """
        self.__modems = modems                              # array of string


    def __len__(self):
        return len(self.__modems)


    # ----------------------------------------------------------------------------------------------------------------

    def modem(self, index):
        return self.__modems[index]


    def number(self, index):
        pieces = self.modem(index).split('/')

        return pieces[-1]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ModemList:{modems:%s}" % self.__modems


# --------------------------------------------------------------------------------------------------------------------

class SIMList(object):
    """
    modem.generic.sim    : /org/freedesktop/ModemManager1/SIM/0
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_mmcli(cls, lines):
        sims = []

        for line in lines:
            match = re.match(r'modem.generic.sim\s+:\s+([\S]+)', line)
            if match:
                sims.append(match.groups()[0])
                break

        return cls(sims)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sims):
        """
        Constructor
        """
        self.__sims = sims                                  # array of string


    def __len__(self):
        return len(self.__sims)


    # ----------------------------------------------------------------------------------------------------------------

    def sim(self, index):
        return self.__sims[index]


    def number(self, index):
        pieces = self.sim(index).split('/')

        return pieces[-1]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SIMList:{sims:%s}" % self.__sims
