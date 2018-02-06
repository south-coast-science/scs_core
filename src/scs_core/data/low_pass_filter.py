"""
Created on 6 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Ten Little Algorithms, Part 2: The Single-Pole Low-Pass Filter
https://www.embeddedrelated.com/showarticle/779.php
"""


# --------------------------------------------------------------------------------------------------------------------

class LowPassFilter(object):
    """
    classdocs
    """

    @classmethod
    def construct(cls, delta_t, cut_off_frequency):
        tau = 1 / cut_off_frequency
        alpha = delta_t / tau

        return LowPassFilter(alpha)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, alpha):
        """
        Constructor
        """
        self.__alpha = alpha
        self.__y = None


    def reset(self):
        self.__y = None


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, x):
        if self.__y is None:
            self.__y = x

        self.__y += self.__alpha * (x - self.__y)

        return self.__y


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LowPassFilter:{alpha:%s, y:%s}" % (self.__alpha, self.__y)
