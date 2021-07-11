"""
Created on 11 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

settings for OPCMonitor

example JSON:
{"model": "N3", "sample-period": 10, "restart-on-zeroes": true, "power-saving": false}
"""

from collections import OrderedDict

from scs_core.data.json import MultiPersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class OPCConf(MultiPersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "opc_conf.json"

    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))

        return cls.conf_dir(), filename


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, name=None, skeleton=False):
        if not jdict:
            return None

        model = jdict.get('model')
        sample_period = jdict.get('sample-period')
        restart_on_zeroes = jdict.get('restart-on-zeroes', True)
        power_saving = jdict.get('power-saving')

        bus = jdict.get('bus')
        address = jdict.get('address')

        return cls(model, sample_period, restart_on_zeroes, power_saving, bus, address, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, sample_period, restart_on_zeroes, power_saving, bus, address, name=None):
        """
        Constructor
        """
        super().__init__(name)

        self.__model = model                                        # string
        self.__sample_period = int(sample_period)                   # int
        self.__restart_on_zeroes = bool(restart_on_zeroes)          # bool
        self.__power_saving = bool(power_saving)                    # bool

        self.__bus = bus                                            # int
        self.__address = address                                    # int


    def __eq__(self, other):                            # ignore name
        try:
            return self.model == other.model and self.sample_period == other.sample_period and \
                   self.restart_on_zeroes == other.restart_on_zeroes and self.power_saving == other.power_saving and \
                   self.bus == other.bus and self.address == other.address

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def opc_monitor(self, interface, host):
        return None


    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def opc(self, interface, host):
        return None


    # noinspection PyMethodMayBeStatic
    def uses_spi(self):
        return True


    def opc_bus(self, host):
        try:
            return int(self.__bus)

        except TypeError:
            return host.opc_spi_bus()


    def opc_address(self, host):
        try:
            return int(self.__address)

        except TypeError:
            return host.opc_spi_device()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def sample_period(self):
        return self.__sample_period


    @property
    def power_saving(self):
        return self.__power_saving


    @property
    def restart_on_zeroes(self):
        return self.__restart_on_zeroes


    @property
    def bus(self):
        return self.__bus


    @property
    def address(self):
        return self.__address


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.model
        jdict['sample-period'] = self.sample_period
        jdict['restart-on-zeroes'] = self.restart_on_zeroes
        jdict['power-saving'] = self.power_saving

        if self.__bus is not None:
            jdict['bus'] = self.bus

        if self.__address is not None:
            jdict['address'] = self.address

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCConf(core):{name:%s, model:%s, sample_period:%s, restart_on_zeroes:%s, power_saving:%s, " \
               "bus:%s, address:%s}" %  \
               (self.name, self.model, self.sample_period, self.restart_on_zeroes, self.power_saving,
                self.bus, self.address)
