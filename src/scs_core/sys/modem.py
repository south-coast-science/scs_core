"""
Created on 24 Mar 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Modem
-----
modem.generic.device-identifier                 : 3f07553c31ce11715037ac16c24ceddcfb6f7a0b
modem.generic.manufacturer                      : QUALCOMM INCORPORATED
modem.generic.model                             : QUECTEL Mobile Broadband Module
modem.generic.revision                          : EC21EFAR06A01M4G
...
modem.3gpp.imei                                 : 867962041294151

example JSON:
{"id": "3f07553c31ce11715037ac16c24ceddcfb6f7a0b", "imei": "867962041294151", "mfr": "QUALCOMM INCORPORATED",
"model": "QUECTEL Mobile Broadband Module", "rev": "EC21EFAR06A01M4G"}


ModemConnection
---------------
modem.generic.state                         : connected
modem.generic.state-failed-reason           : --
modem.generic.signal-quality.value          : 67
modem.generic.signal-quality.recent         : yes

example JSON:
{"state": "connected", "signal": {"quality": 67, "recent": true}}


SIM (Subscriber Identity Module)
--------------------------------
sim.dbus-path                               : /org/freedesktop/ModemManager1/SIM/0
sim.properties.imsi                         : 234104886708667
sim.properties.iccid                        : 8944110068256270054
sim.properties.operator-code                : 23410
sim.properties.operator-name                : giffgaff
sim.properties.emergency-numbers.length     : 2
sim.properties.emergency-numbers.value[1]   : 999
sim.properties.emergency-numbers.value[2]   : 00112

example JSON:
{"imsi": "123", "iccid": "456", "operator-code": "789 012", "operator-name": "giff gaff"}
"""

import re

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


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
            match = re.match(r'modem-list.value\[\d+]\s+:\s+(\S+)', line)
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

class Modem(JSONable):
    """
    modem.generic.device-identifier                 : 3f07553c31ce11715037ac16c24ceddcfb6f7a0b
    modem.generic.manufacturer                      : QUALCOMM INCORPORATED
    modem.generic.model                             : QUECTEL Mobile Broadband Module
    modem.generic.revision                          : EC21EFAR06A01M4G
    ...
    modem.3gpp.imei                                 : 867962041294151
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        id = jdict.get('id')
        imei = jdict.get('imei')
        mfr = jdict.get('mfr')
        model = jdict.get('model')
        rev = jdict.get('rev')

        return cls(id, imei, mfr, model, rev)


    @classmethod
    def construct_from_mmcli(cls, lines):
        id = None
        imei = None
        mfr = None
        model = None
        rev = None

        for line in lines:
            match = re.match(r'modem\.generic\.device-identifier\s+:\s+(\S+)', line)
            if match:
                id = match.groups()[0]
                continue

            match = re.match(r'.*\.imei\s+:\s+(\d+)', line)
            if match:
                imei = match.groups()[0]
                continue

            match = re.match(r'modem\.generic\.manufacturer\s+:\s+(\S.*\S)', line)
            if match:
                mfr = match.groups()[0]
                continue

            match = re.match(r'modem\.generic\.model\s+:\s+(\S.*\S)', line)
            if match:
                model = match.groups()[0]
                continue

            match = re.match(r'modem\.generic\.revision\s+:\s+(\S+)', line)
            if match:
                rev = match.groups()[0]
                continue

        return cls(id, imei, mfr, model, rev)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, imei, mfr, model, rev):
        """
        Constructor
        """
        self.__id = id                              # string
        self.__imei = imei                          # string
        self.__mfr = mfr                            # string
        self.__model = model                        # string
        self.__rev = rev                            # string


    def __eq__(self, other):
        try:
            return self.id == other.id and self.imei == other.imei and self.mfr == other.mfr and \
                   self.model == other.model and self.rev == other.rev

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def imei(self):
        return self.__imei


    @property
    def mfr(self):
        return self.__mfr


    @property
    def model(self):
        return self.__model


    @property
    def rev(self):
        return self.__rev


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['id'] = self.id
        jdict['imei'] = self.imei
        jdict['mfr'] = self.mfr
        jdict['model'] = self.model
        jdict['rev'] = self.rev

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Modem:{id:%s, imei:%s, mfr:%s, model:%s, rev:%s}" %  \
               (self.id, self.imei, self.mfr, self.model, self.rev)


# --------------------------------------------------------------------------------------------------------------------

class ModemConnection(JSONable):
    """
    modem.generic.state                         : connected
    modem.generic.state-failed-reason           : --
    modem.generic.signal-quality.value          : 67
    modem.generic.signal-quality.recent         : yes
    """

    UNAVAILABLE_STATE = "unavailable"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        state = jdict.get('state')
        failure = jdict.get('failure')
        signal = Signal.construct_from_jdict(jdict.get('signal'))

        return cls(state, failure, signal)


    @classmethod
    def construct_from_mmcli(cls, lines):
        state = None
        failure = None
        quality = None
        recent = None

        for line in lines:
            match = re.match(r'modem\.generic\.state\s+:\s+([a-z]+)', line)
            if match:
                state = match.groups()[0]
                continue

            match = re.match(r'modem\.generic\.state-failed-reason\s+:\s+(\S.*\S)', line)
            if match:
                reported_failure = match.groups()[0]
                failure = None if reported_failure == '--' else reported_failure
                continue

            match = re.match(r'modem\.generic\.signal-quality\.value\s+:\s+(\d+)', line)
            if match:
                quality = match.groups()[0]
                continue

            match = re.match(r'modem\.generic\.signal-quality\.recent\s+:\s+([a-z]+)', line)
            if match:
                recent = match.groups()[0] == 'yes'
                continue

        return cls(state, failure, Signal(quality, recent))


    @classmethod
    def null_datum(cls):
        return cls(cls.UNAVAILABLE_STATE, None, Signal.null_datum())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, state, failure, signal):
        """
        Constructor
        """
        self.__state = state                            # string
        self.__failure = failure                        # string
        self.__signal = signal                          # Signal


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def state(self):
        return self.__state


    @property
    def failure(self):
        return self.__failure


    @property
    def signal(self):
        return self.__signal


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['state'] = self.state

        if self.failure is not None:
            jdict['failure'] = self.failure

        jdict['signal'] = self.signal

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ModemConnection:{state:%s, failure:%s, signal:%s}" %  (self.state, self.failure, self.signal)


# --------------------------------------------------------------------------------------------------------------------

class Signal(JSONable):
    """
    modem.generic.signal-quality.value          : 67
    modem.generic.signal-quality.recent         : yes
    """

    __SIGNIFICANT_QUALITY_DIFFERENCE = 10

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        quality = jdict.get('quality')
        recent = jdict.get('recent')

        return cls(quality, recent)


    @classmethod
    def null_datum(cls):
        return cls(None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, quality, recent):
        """
        Constructor
        """
        self.__quality = Datum.int(quality)                 # int
        self.__recent = recent                              # bool


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def quality(self):
        return self.__quality


    @property
    def recent(self):
        return self.__recent


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['quality'] = self.quality
        jdict['recent'] = self.recent

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Signal:{quality:%s, recent:%s}" %  (self.quality, self.recent)


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
            match = re.match(r'modem\.generic\.sim\s+:\s+(\S+)', line)
            if match:
                sims.append(match.groups()[0])

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
            match = re.match(r'sim\.properties\.imsi\s+:\s+(\d+)', line)
            if match:
                imsi = match.groups()[0]
                continue

            match = re.match(r'sim\.properties\.iccid\s+:\s+(\d+)', line)
            if match:
                iccid = match.groups()[0]
                continue

            match = re.match(r'sim\.properties\.operator-code\s+:\s+(\d+)', line)
            if match:
                operator_code = match.groups()[0]
                continue

            match = re.match(r'sim\.properties\.operator-name\s+:\s+(\S.*)', line)
            if match:
                reported_name = match.groups()[0].strip()
                operator_name = None if reported_name == '--' else reported_name

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
