"""
Created on 18 Sep 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A high-performance linear regression utility requiring scipy

https://www.w3schools.com/python/python_ml_linear_regression.asp
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class LinRegress(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, x, y, prec=6):
        from scipy import stats                     # late import

        if len(x) != len(y):
            raise ValueError("len x (%d) is not the same as len y (%d)" % (len(x), len(y)))

        slope, intercept, r, p, std_err = stats.linregress(x, y)

        return cls(len(x), round(slope, prec), round(intercept, prec), round(r**2, prec), round(p, prec),
                   round(std_err, prec))


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        count = jdict.get('count')
        slope = jdict.get('slope')
        intercept = jdict.get('intercept')
        r2 = jdict.get('r2')
        p = jdict.get('p')
        std_err = jdict.get('std-err')

        return cls(count, slope, intercept, r2, p, std_err)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, count, slope, intercept, r2, p, std_err):
        """
        Constructor
        """
        self.__count = count                            # int

        self.__slope = slope                            # float
        self.__intercept = intercept                    # float
        self.__r2 = r2                                  # float
        self.__p = p                                    # float
        self.__std_err = std_err                        # float


    def __len__(self):
        return self.__count


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def slope(self):
        return self.__slope


    @property
    def intercept(self):
        return self.__intercept


    @property
    def r2(self):
        return self.__r2


    @property
    def p(self):
        return self.__p


    @property
    def std_err(self):
        return self.__std_err


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['count'] = len(self)

        jdict['slope'] = self.slope
        jdict['intercept'] = self.intercept
        jdict['r2'] = self.r2
        jdict['p'] = self.p
        jdict['std-err'] = self.std_err

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LinRegress:{slope:%s, intercept:%s, r2:%s, p:%s, std_err:%s}" %  \
               (self.slope, self.intercept, self.r2, self.p, self.std_err)
