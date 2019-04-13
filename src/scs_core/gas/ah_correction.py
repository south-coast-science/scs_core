"""
Created on 1 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

corrected_sensitivity = (1 + (aH * wS)) * sensitivity   ~ NOT aH / wS !
corrected_baseline_offset = (aH * wB) + baseline_offset

corrected_concentration = (weC / corrected_sensitivity) - corrected_baseline_offset

corrected_sensitivity = -0.0152 * aH + 0.2942
corrected_baseline_offset = -0.2727 * aH - 0.5773

"""

import sys


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

    # def compute(self, we_c, ah):
    #     corrected_sensitivity = (1 + (ah * self.__ws)) * self.__sensitivity
    #     corrected_baseline_offset = (ah * self.__wb) + self.__baseline_offset
    #
    #     cnc = (we_c / corrected_sensitivity) - corrected_baseline_offset
    #
    #     return cnc

    def ah_corr(self, cnc, ah):
        # no correction...
        # cnc = we_c / (0.290 / 1000.0)

        # aH factors...
        # m_ah = (-0.0505 * ah) + 1.0036      # corr1
        # m_ah = (-0.0252 * ah) + 1.0036      # corr2
        m_ah = (-0.0126 * ah) + 1.0036      # corr3

        c_ah = (-0.9095 * ah) + 30.838

        cnc_corr = (cnc - c_ah) / m_ah

        print("cnc:%0.1f cnc_corr:%0.1f ah: %0.3f m_ah: %0.3f c_ah: %0.3f" %
              (cnc, cnc_corr, ah, m_ah, c_ah),
              file=sys.stderr)

        return cnc_corr


    def rh_corr(self, cnc, rh, t):
        # t factors...
        # t_err = (-1.9546 * t) + 35.04
        t_err = (-1.8 * t) + 35.097

        t_comp_cnc = cnc - t_err


        # aH factors...
        m_rh = (0.0042 * rh) + 0.3978      # corr1

        c_rh = (0.2535 * rh) + 5.0848

        cnc_corr = (t_comp_cnc - c_rh) / m_rh

        print("cnc:%0.1f rh: %0.3f t:%0.1f - t_err:%0.3f t_comp_cnc:%0.1f - m_rh: %0.3f c_rh: %0.3f - cnc_corr:%0.1f " %
              (cnc, rh, t, t_err, t_comp_cnc, m_rh, c_rh, cnc_corr),
              file=sys.stderr)

        return t_comp_cnc, m_rh, c_rh, cnc_corr

    # def compute(self, we_c, ah):
    #     corrected_sens = (-0.0152 * ah) + 0.2942                # mV
    #     corrected_baseline_offset = (-0.909 * ah) + 30.8        # ppb
    #
    #     print("we_c: %0.6f ah: %0.3f m: %0.3f c: %0.3f" % (we_c, ah, corrected_sens, corrected_baseline_offset),
    #           file=sys.stderr)
    #
    #     cnc = (we_c / (corrected_sens / 1000.0)) - corrected_baseline_offset
    #
    #     return cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AhCorrection:{sensitivity:%s, baseline_offset:%s, ws:%s, wb:%s}" %  \
               (self.__sensitivity, self.__baseline_offset, self.__ws, self.__wb)
