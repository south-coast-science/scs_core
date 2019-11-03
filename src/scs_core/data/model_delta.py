"""
Created on 2 Nov 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

one cell of a statistical model, with one independent variable and one or more dependent variables
"""

from collections import OrderedDict
from statistics import stdev

from scs_core.data.json import JSONable
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class ModelDelta(JSONable):
    """
    classdocs
    """

    DEFAULT_INDEPENDENT_PREC =      1
    DEFAULT_DEPENDENT_PREC =        3

    __STDEV_PRECISION =             3

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, ind_name, ind_prec, dep_names, dep_prec):
        dependents = OrderedDict()
        for dep_name in dep_names:
            dependents[dep_name] = []

        return ModelDelta(ind_name, [], ind_prec, dependents, dep_prec)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ind_name, ind_values, ind_prec, dependents, dep_prec):
        """
        Constructor
        """
        self.__ind_name = ind_name                              # string
        self.__ind_values = ind_values                          # array of float
        self.__ind_prec = ind_prec                              # int precision

        self.__dependents = dependents                          # dict of string: array of float
        self.__dep_prec = dep_prec                              # int precision


    def __len__(self):
        return len(self.__ind_values)


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, ind_value, dependents):
        if len(dependents) != len(self.__dependents):
            raise IndexError("number of dependents given:%d required:%d" % (len(dependents), len(self.__dependents)))

        self.__ind_values.append(ind_value)

        for key in dependents.keys():
            self.__dependents[key].append(dependents[key])


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = PathDict()

        jdict.append('samples', len(self))

        jdict.append(self.ind_name + '.min', self.ind_min())
        jdict.append(self.ind_name + '.avg', self.ind_avg())
        jdict.append(self.ind_name + '.max', self.ind_max())

        for name in self.dep_names:
            jdict.append(name + '.avg', self.dep_avg(name))
            jdict.append(name + '.stdev', self.dep_stdev(name))

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def ind_min(self):
        value = min(self.__ind_values)
        return round(value, self.__ind_prec)


    def ind_avg(self):
        value = sum(self.__ind_values) / len(self)
        return round(value, self.__ind_prec)


    def ind_max(self):
        value = max(self.__ind_values)
        return round(value, self.__ind_prec)


    def dep_avg(self, name):
        value = sum(self.__dependents[name]) / len(self)
        return round(value, self.__dep_prec)


    def dep_stdev(self, name):
        value = stdev(self.__dependents[name])
        return round(value, self.__STDEV_PRECISION)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def ind_name(self):
        return self.__ind_name


    @property
    def dep_names(self):
        return self.__dependents.keys()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ModelDelta:{independent:%s, ind_prec:%s, dependents:%s, dep_prec:%s, length:%d}" % \
               (self.ind_name, self.__ind_prec, self.dep_names, self.__dep_prec, len(self))
