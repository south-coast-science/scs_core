"""
Created on 1 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

corrected_baseline = (aH * wB) + baseline
corrected_sensitivity = (1 + (aH / wS)) * sensitivity
"""


# --------------------------------------------------------------------------------------------------------------------

class AhCorrection(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensitivity, baseline, ws, wb):
        """
        Constructor
        """
        self.__sensitivity = sensitivity
        self.__baseline = baseline

        self.__ws = ws
        self.__wb = wb


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, we_c, ah):
        corrected_baseline = (ah * self.__wb) + self.__baseline
        corrected_sensitivity = (1 + (ah / self.__ws)) * self.__sensitivity

        cnc = (we_c / corrected_sensitivity) - corrected_baseline

        return cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AhCorrection:{sensitivity:%s, baseline:%s, ws:%s, wb:%s}" %  \
               (self.__sensitivity, self.__baseline, self.__ws, self.__wb)
