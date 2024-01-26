"""
Created on 25 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class ModelMap(object):
    """
    classdocs
    """

    __MAPS =       {}

    @classmethod
    def init(cls):
        cls.__MAPS['oE.1'] = cls('oE.1', 'oE.1', 'oE.1', 'g0')
        cls.__MAPS['oM.2'] = cls('oM.2', 'oE.1', 'oPG.2', 'oP.2')
        cls.__MAPS['uE.1'] = cls('uE.1', 'uE.1', 'uE.1', 'g0')


    @classmethod
    def map(cls, name):
        return cls.__MAPS[name]                             # may raise KeyError


    @classmethod
    def names(cls):
        return sorted(cls.__MAPS.keys())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, gas_compendium_group, pg_gg_ml_template, p_gg_ml_template):
        """
        Constructor
        """
        self.__name = name                                                  # string

        self.__gas_compendium_group = gas_compendium_group                  # string
        self.__pg_gg_ml_template = pg_gg_ml_template                        # string PMx + Gas
        self.__p_gg_ml_template = p_gg_ml_template                          # string PMx


    def __eq__(self, other):
        try:
            return self.name == other.name and self.gas_compendium_group == other.gas_compendium_group and \
                   self.pg_gg_ml_template == other.pg_gg_ml_template and self.p_gg_ml_template == other.p_gg_ml_template

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def gas_compendium_group(self):
        return self.__gas_compendium_group


    @property
    def pg_gg_ml_template(self):
        return self.__pg_gg_ml_template


    @property
    def p_gg_ml_template(self):
        return self.__p_gg_ml_template


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ModelMap:{name:%s, gas_compendium_group:%s, pg_gg_ml_template:%s, p_gg_ml_template:%s}" %  \
               (self.name, self.gas_compendium_group, self.pg_gg_ml_template, self.p_gg_ml_template)
