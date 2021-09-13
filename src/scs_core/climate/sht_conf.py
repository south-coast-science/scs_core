"""
Created on 13 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

the I2C addresses of the internal (in A4 pot) and external (exposed to air) SHTs

example JSON:
{"int": "0x44", "ext": "0x45"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class SHTConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "sht_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __addr_str(cls, addr):
        if addr is None:
            return None

        return "0x%02x" % addr


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        int_str = jdict.get('int')
        ext_str = jdict.get('ext')

        int_addr = None if int_str is None else int(int_str, 0)
        ext_addr = None if ext_str is None else int(ext_str, 0)

        return cls(int_addr, ext_addr)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, int_addr, ext_addr):
        """
        Constructor
        """
        super().__init__()

        self.__int_addr = int_addr          # int       I2C address of SHT in A4 package
        self.__ext_addr = ext_addr          # int       I2C address of SHT exposed to air


    def __eq__(self, other):
        try:
            return self.int_addr == other.int_addr and self.ext_addr == other.ext_addr

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyMethodMayBeStatic
    def int_sht(self):
        return None


    # noinspection PyMethodMayBeStatic
    def ext_sht(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def int_addr(self):
        return self.__int_addr


    @property
    def ext_addr(self):
        return self.__ext_addr


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['int'] = SHTConf.__addr_str(self.__int_addr)
        jdict['ext'] = SHTConf.__addr_str(self.__ext_addr)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SHTConf(core):{int_addr:%s, ext_addr:%s}" %  \
               (SHTConf.__addr_str(self.int_addr), SHTConf.__addr_str(self.ext_addr))
