"""
Created on 1 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

corrected_sensitivity = (1 + (aH * wS)) * sensitivity   ~ NOT aH / wS !
corrected_baseline_offset = (aH * wB) + baseline_offset

corrected_concentration = (weC / corrected_sensitivity) - corrected_baseline_offset
"""


# --------------------------------------------------------------------------------------------------------------------

class AhCorrection(object):
    """
    classdocs
    """

    @classmethod
    def construct(cls, sens_mv, baseline_offset, ws, wb):
        sensitivity = sens_mv / 1000.0

        return cls(sensitivity, baseline_offset, ws, wb)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensitivity, baseline_offset, ws, wb):
        """
        Constructor
        """
        self.__sensitivity = float(sensitivity)                     # float         V / ppb
        self.__baseline_offset = float(baseline_offset)             # float         ppb

        self.__ws = float(ws)                                       # float         (V / ppb) / (g / m3)
        self.__wb = float(wb)                                       # float         ppb / (g / m3)


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, we_c, ah):
        corrected_sensitivity = (1 + (ah * self.__ws)) * self.__sensitivity
        corrected_baseline_offset = (ah * self.__wb) + self.__baseline_offset

        cnc = (we_c / corrected_sensitivity) - corrected_baseline_offset

        return cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AhCorrection:{sensitivity:%s, baseline_offset:%s, ws:%s, wb:%s}" %  \
               (self.__sensitivity, self.__baseline_offset, self.__ws, self.__wb)
