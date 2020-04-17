"""
Created on 15 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class SampleDelta(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def deltas(cls, domain_lower, domain_upper, delta):
        return [cls(lower_bound, lower_bound + delta) for lower_bound in range(domain_lower, domain_upper, delta)]


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lower_bound, upper_bound):
        """
        Constructor
        """
        if upper_bound < lower_bound:
            raise ValueError((lower_bound, upper_bound))

        self.__lower_bound = int(lower_bound)                       # int
        self.__upper_bound = int(upper_bound)                       # int


    # ----------------------------------------------------------------------------------------------------------------

    def includes(self, value):
        if value is None:
            return False

        return self.lower_bound <= value < self.upper_bound


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def lower_bound(self):
        return self.__lower_bound


    @property
    def upper_bound(self):
        return self.__upper_bound


    # ----------------------------------------------------------------------------------------------------------------

    def description(self):
        return '-'.join((str(self.lower_bound), str(self.upper_bound)))


    def __str__(self, *args, **kwargs):
        return "SampleDelta:{lower_bound:%s, upper_bound:%s}" %  (self.lower_bound, self.upper_bound)
