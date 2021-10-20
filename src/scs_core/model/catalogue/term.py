"""
Created on 22 Sep 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Term(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, path, values, prec=6):
        minimum = min(values)
        average = sum(values) / len(values)
        maximum = max(values)

        return cls(path, round(minimum, prec), round(average, prec), round(maximum, prec))


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        path = jdict.get('path')

        minimum = jdict.get('min')
        average = jdict.get('avg')
        maximum = jdict.get('max')

        return cls(path, minimum, average, maximum)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, minimum, average, maximum):
        """
        Constructor
        """
        self.__path = path                              # string

        self.__minimum = minimum                        # float
        self.__average = average                        # float
        self.__maximum = maximum                        # float


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


    @property
    def minimum(self):
        return self.__minimum


    @property
    def average(self):
        return self.__average


    @property
    def maximum(self):
        return self.__maximum


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['path'] = self.path

        jdict['min'] = self.minimum
        jdict['avg'] = self.average
        jdict['max'] = self.maximum

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Term:{path:%s, minimum:%s, average:%s, maximum:%s}" %  \
               (self.path, self.minimum, self.average, self.maximum)


# --------------------------------------------------------------------------------------------------------------------

class PrimaryTerm(Term):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, minimum, average, maximum):
        """
        Constructor
        """
        super().__init__(path, minimum, average, maximum)


    # ----------------------------------------------------------------------------------------------------------------

    def preprocess(self, node, offset):
        try:
            value = float(node)
        except (TypeError, ValueError):
            return None, 0

        baselined_value = value + offset                # a positive offset causes the value to be raised

        if baselined_value > self.maximum:
            return self.maximum, baselined_value - self.maximum

        return baselined_value, 0


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PrimaryTerm:{path:%s, minimum:%s, average:%s, maximum:%s}" %  \
               (self.path, self.minimum, self.average, self.maximum)


# --------------------------------------------------------------------------------------------------------------------

class SecondaryTerm(Term):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, minimum, average, maximum):
        """
        Constructor
        """
        super().__init__(path, minimum, average, maximum)


    # ----------------------------------------------------------------------------------------------------------------

    def is_in_bounds(self, node):
        try:
            value = float(node)
        except (TypeError, ValueError):
            return False

        return self.minimum <= value <= self.maximum


    def preprocess(self, node):
        try:
            value = float(node)
        except (TypeError, ValueError):
            return None

        if value < self.minimum:
            return self.minimum

        if value > self.maximum:
            return self.maximum

        return value


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SecondaryTerm:{path:%s, minimum:%s, average:%s, maximum:%s}" %  \
               (self.path, self.minimum, self.average, self.maximum)
