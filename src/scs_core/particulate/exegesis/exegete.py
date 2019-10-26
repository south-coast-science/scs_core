"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a catalogue of particulate exegesis models
"""

from scs_core.particulate.exegesis.isece001 import ISECEv1


# --------------------------------------------------------------------------------------------------------------------

class Exegete(object):
    """
    classdocs
    """

    __ROOT = 'exg'

    @classmethod
    def root(cls):
        return cls.__ROOT


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def models():
        return [ISECEv1.name()]


    @staticmethod
    def model(name, host):
        if name == ISECEv1.name():
            return ISECEv1.load(host)

        raise ValueError(name)
