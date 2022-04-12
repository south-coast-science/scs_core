"""
Created on 3 Mar 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://en.wikipedia.org/wiki/Standard_deviation

example document:
{"err": {"SO2": {"vE": {"Urban": {"22Q1": {"count": 14167, "min": -239.8, "mean": 0.1, "median": 0.1, "max": 145.0,
"var": 19.5, "stdev": 4.4, "stdev2": 8.8, "stdev3": 13.2}}}}}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Stats(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, values, prec=3):
        import statistics                               # late import

        minimum = round(min(values), prec)
        mean = round(statistics.mean(values), prec)
        median = round(statistics.median(values), prec)
        maximum = round(max(values), prec)

        variance = round(statistics.variance(values, xbar=mean), prec)

        stdev = round(statistics.stdev(values), prec)
        stdev2 = round(stdev * 2.0, prec)
        stdev3 = round(stdev * 3.0, prec)

        return cls(len(values), minimum, mean, median, maximum, variance, stdev, stdev2, stdev3)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        count = jdict.get('count')

        minimum = jdict.get('min')
        mean = jdict.get('mean')
        median = jdict.get('median')
        maximum = jdict.get('max')

        variance = jdict.get('var')

        stdev = jdict.get('stdev')
        stdev2 = jdict.get('stdev2')
        stdev3 = jdict.get('stdev3')

        return cls(count, minimum, mean, median, maximum, variance, stdev, stdev2, stdev3)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, count, minimum, mean, median, maximum, variance, stdev, stdev2, stdev3):
        """
        Constructor
        """
        self.__count = count                            # int

        self.__minimum = minimum                        # float
        self.__mean = mean                              # float
        self.__median = median                          # float
        self.__maximum = maximum                        # float

        self.__variance = variance                      # float

        self.__stdev = stdev                            # float
        self.__stdev2 = stdev2                          # float
        self.__stdev3 = stdev3                          # float


    def __len__(self):
        return self.count


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['count'] = self.count

        jdict['min'] = self.minimum
        jdict['mean'] = self.mean
        jdict['median'] = self.median
        jdict['max'] = self.maximum

        jdict['var'] = self.variance

        jdict['stdev'] = self.stdev
        jdict['stdev2'] = self.stdev2
        jdict['stdev3'] = self.stdev3

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def lower1(self):
        return self.median - self.stdev


    def lower2(self):
        return self.median - self.stdev2


    def lower3(self):
        return self.median - self.stdev3


    def upper1(self):
        return self.median + self.stdev


    def upper2(self):
        return self.median + self.stdev2


    def upper3(self):
        return self.median + self.stdev3


    def amp1(self):
        return self.upper1() - self.lower1()


    def amp2(self):
        return self.upper2() - self.lower2()


    def amp3(self):
        return self.upper3() - self.lower3()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def count(self):
        return self.__count


    @property
    def minimum(self):
        return self.__minimum


    @property
    def mean(self):
        return self.__mean


    @property
    def median(self):
        return self.__median


    @property
    def maximum(self):
        return self.__maximum


    @property
    def variance(self):
        return self.__variance


    @property
    def stdev(self):
        return self.__stdev


    @property
    def stdev2(self):
        return self.__stdev2


    @property
    def stdev3(self):
        return self.__stdev3


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Stats:{minimum:%s, mean:%s, median:%s, maximum:%s, variance:%s, stdev:%s, stdev2:%s, stdev3:%s}" %  \
               (self.minimum, self.mean, self.median, self.maximum, self.variance, self.stdev, self.stdev2, self.stdev3)
