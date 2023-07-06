"""
Created on 11 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

settings for OPCMonitor

example JSON:
{"model": "N3", "sample-period": 10, "restart-on-zeroes": true, "power-saving": false,
"custom-dev-path": "/dev/spi/by-connector/H3"}
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


    @classmethod
    def load(cls, manager, name=None, encryption_key=None, skeleton=False):
        conf = super().load(manager, name=name, encryption_key=encryption_key, skeleton=skeleton)

        if conf:
            conf.__default_dev_path = manager.opc_spi_dev_path()

        return conf


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, name=None, skeleton=False):
        if not jdict:
            return None

        model = jdict.get('model')
        sample_period = jdict.get('sample-period')
        restart_on_zeroes = jdict.get('restart-on-zeroes', True)
        power_saving = jdict.get('power-saving')

        custom_dev_path = jdict.get('custom-dev-path')

        return cls(model, sample_period, restart_on_zeroes, power_saving, custom_dev_path, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, sample_period, restart_on_zeroes, power_saving, custom_dev_path, name=None):
        """
        Constructor
        """
        super().__init__(name)

        self.__model = model                                        # string
        self.__sample_period = int(sample_period)                   # int
        self.__restart_on_zeroes = bool(restart_on_zeroes)          # bool
        self.__power_saving = bool(power_saving)                    # bool

        self.__default_dev_path = None                              # string
        self.__custom_dev_path = custom_dev_path                    # string


    def __eq__(self, other):                            # ignore name
        try:
            return self.model == other.model and self.sample_period == other.sample_period and \
                   self.restart_on_zeroes == other.restart_on_zeroes and self.power_saving == other.power_saving and \
                   self.custom_dev_path == other.custom_dev_path

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def opc_monitor(self, interface):
        return None


    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def opc(self, interface):
        return None


    # noinspection PyMethodMayBeStatic
    def uses_spi(self):
        return True


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
    def dev_path(self):
        return self.default_dev_path if self.custom_dev_path is None else self.custom_dev_path


    @property
    def default_dev_path(self):
        return self.__default_dev_path


    @property
    def custom_dev_path(self):
        return self.__custom_dev_path


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.model
        jdict['sample-period'] = self.sample_period
        jdict['restart-on-zeroes'] = self.restart_on_zeroes
        jdict['power-saving'] = self.power_saving

        if self.custom_dev_path is not None:
            jdict['custom-dev-path'] = self.custom_dev_path

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCConf(core):{name:%s, model:%s, sample_period:%s, restart_on_zeroes:%s, power_saving:%s, " \
               "default_dev_path:%s, custom_dev_path:%s}" %  \
               (self.name, self.model, self.sample_period, self.restart_on_zeroes, self.power_saving,
                self.default_dev_path, self.custom_dev_path)
