"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a catalogue of particulates exegesis models
"""

from scs_core.particulate.exegesis.isece001 import ISECEv1


# --------------------------------------------------------------------------------------------------------------------

class Exegete(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def models():
        return [ISECEv1.name()]


    @staticmethod
    def model(name, host):
        if name == ISECEv1.name():
            return ISECEv1.load(host)

        raise ValueError(name)
