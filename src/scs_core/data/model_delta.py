"""
Created on 2 Nov 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

one cell of a statistical model, with one independent variable and one or more dependent variables

https://en.wikipedia.org/wiki/Dependent_and_independent_variables

example:
{"domain": "70.0 - 75.0", "praxis": {"climate": {"val": {"hmd": {"min": 70.0, "avg": 72.6, "max": 74.9}}}},
"error": {"pm1": {"avg": 2.648, "stdev": 2.458}, "pm2p5": {"avg": 2.992, "stdev": 2.652},
"pm10": {"avg": 2.77, "stdev": 2.456}}, "samples": 2307}
"""

from collections import OrderedDict
from statistics import mean, stdev

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
    def construct(cls, domain_min, domain_max, ind_name, ind_prec, dep_names, dep_prec):
        dependents = OrderedDict()
        for dep_name in dep_names:
            dependents[dep_name] = []

        return ModelDelta(domain_min, domain_max, ind_name, [], ind_prec, dependents, dep_prec)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, domain_min, domain_max, ind_name, ind_values, ind_prec, dependents, dep_prec):
        """
        Constructor
        """
        self.__domain_min = domain_min                          # float
        self.__domain_max = domain_max                          # float

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

        jdict.append('domain', self.domain())
        jdict.append('domain-midpoint', self.domain_midpoint())

        jdict.append(self.ind_name + '.min', self.ind_min())
        jdict.append(self.ind_name + '.avg', self.ind_avg())
        jdict.append(self.ind_name + '.max', self.ind_max())

        for name in self.dep_names:
            jdict.append(name + '.avg', self.dep_avg(name))
            jdict.append(name + '.stdev', self.dep_stdev(name))

        jdict.append('samples', len(self))

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def ind_min(self):
        if not self.__ind_values:
            return None

        value = min(self.__ind_values)
        return round(value, self.__ind_prec)


    def ind_avg(self):
        if not self.__ind_values:
            return None

        value = sum(self.__ind_values) / len(self)
        return round(value, self.__ind_prec)


    def ind_max(self):
        if not self.__ind_values:
            return None

        value = max(self.__ind_values)
        return round(value, self.__ind_prec)


    def dep_avg(self, name):
        if not self.__dependents[name]:
            return None

        value = sum(self.__dependents[name]) / len(self)
        return round(value, self.__dep_prec)


    def dep_stdev(self, name):
        if not self.__dependents[name] or len(self.__dependents[name]) == 1:
            return None

        value = stdev(self.__dependents[name])
        return round(value, self.__STDEV_PRECISION)


    # ----------------------------------------------------------------------------------------------------------------

    def domain(self):
        return ' - '.join((str(round(self.domain_min, 1)), str(round(self.domain_max, 1))))


    def domain_midpoint(self):
        return round(mean((self.domain_min, self.domain_max)), 1)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def domain_min(self):
        return self.__domain_min


    @property
    def domain_max(self):
        return self.__domain_max


    @property
    def ind_name(self):
        return self.__ind_name


    @property
    def dep_names(self):
        return tuple(self.__dependents.keys())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ModelDelta:{domain:%s, ind_name:%s, ind_prec:%s, dependents:%s, dep_prec:%s, length:%d}" % \
               (self.domain(), self.ind_name, self.__ind_prec, self.dep_names, self.__dep_prec, len(self))
