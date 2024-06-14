"""
Created on 7 June 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A catalogue entry for a machine learning model, for a specific PM size and model

document example:
<see scs_core.aws.model.pmx.compendia>
"""

import os

from collections import OrderedDict

from scs_core.data.json import JSONable, JSONCatalogueEntry
from scs_core.data.lin_regress import LinRegress
from scs_core.data.path_dict import PathDict
from scs_core.data.str import Str

from scs_core.model.catalogue.term import PrimaryTerm, SecondaryTerm, Term
from scs_core.model.catalogue.training_period import TrainingPeriod

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class ReferenceCompendium(JSONable):
    """
    classdocs
    """

    REFERENCE_ENVIRONMENT = [
        'temp',
        'rh',
        'pres'
    ]

    @classmethod
    def is_target(cls, prefix, path, target):
        return cls.__is_term(prefix, path, [target.lower()])


    @classmethod
    def is_environment(cls, prefix, path):
        return cls.__is_term(prefix, path, cls.REFERENCE_ENVIRONMENT)


    @classmethod
    def __is_term(cls, prefix, path, term_set):
        if not path.startswith(prefix):
            return False

        return Term.suffix(prefix, path).lower() in term_set


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, prefix, target_path, reference_targets, reference_environments):
        target = Term.construct(target_path, reference_targets, prec=1)

        environment = {Term.suffix(prefix, path): Term.construct(path, values, prec=3)
                       for path, values in reference_environments.items()}

        return cls(target, environment)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        target = jdict.get('target')

        environment = {path: SecondaryTerm.construct_from_jdict(term_jdict)
                       for path, term_jdict in jdict.get('environment').items()}

        return cls(target, environment)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, target, environment):
        """
        Constructor
        """
        self.__target = target                          # Term
        self.__environment = environment                # dict of path: Term


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def target(self):
        return self.__target


    @property
    def environment(self):
        return self.__environment


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['target'] = self.target
        jdict['environment'] = self.environment

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ReferenceCompendium:{target:%s, environment:%s}" % (self.target, self.environment)


# --------------------------------------------------------------------------------------------------------------------

class ModelCompendium(JSONCatalogueEntry):
    """
    classdocs
    """

    DEVICE_PRIMARIES = [
        'pmx.val.bin:0',
        'pmx.val.bin:1',
        'pmx.val.bin:2',
        'pmx.val.bin:3',
        'pmx.val.bin:4',
        'pmx.val.bin:5',
        'pmx.val.bin:6',
        'pmx.val.bin:7',
        'pmx.val.bin:8',
        'pmx.val.bin:9',
        'pmx.val.bin:10',
        'pmx.val.bin:11',
        'pmx.val.bin:12',
        'pmx.val.bin:13',
        'pmx.val.bin:14',
        'pmx.val.bin:15',
        'pmx.val.bin:16',
        'pmx.val.bin:17',
        'pmx.val.bin:18',
        'pmx.val.bin:19',
        'pmx.val.bin:20',
        'pmx.val.bin:21',
        'pmx.val.bin:22',
        'pmx.val.bin:23'
    ]

    DEVICE_VB_SECONDARIES = [
        'meteo.val.hmd.cur',
        'meteo.val.hmd.slp15min',
        'meteo.val.tmp.cur',
        'meteo.val.tmp.slp15min',
        'pmx.val.mtf1',
        'pmx.val.mtf3',
        'pmx.val.mtf5',
        'pmx.val.mtf7',
        'pmx.val.sfr',
        'pmx.val.sht.hmd.cur',
        'pmx.val.sht.hmd.slp15min',
        'pmx.val.sht.tmp.cur',
        'pmx.val.sht.tmp.slp15min'
    ]

    DEVICE_VE_SECONDARIES = [
        'meteo.exg.val.hmd.cur',
        'meteo.exg.val.hmd.slp15min',
        'meteo.val.tmp.cur',
        'meteo.val.tmp.slp15min',
        'pmx.val.mtf1',
        'pmx.val.mtf3',
        'pmx.val.mtf5',
        'pmx.val.mtf7',
        'pmx.val.sfr',
        'pmx.val.sht.hmd.cur',
        'pmx.val.sht.hmd.slp15min',
        'pmx.val.sht.tmp.cur',
        'pmx.val.sht.tmp.slp15min'
    ]

    DEVICE_SECONDARIES = {
        'vB': DEVICE_VB_SECONDARIES,
        'vE': DEVICE_VE_SECONDARIES
    }

    @classmethod
    def is_primary(cls, prefix, path):
        return cls.__is_term(prefix, path, cls.DEVICE_PRIMARIES)


    @classmethod
    def is_secondary(cls, prefix, path, model_interface):
        return cls.__is_term(prefix, path, cls.DEVICE_SECONDARIES[model_interface])


    @classmethod
    def __is_term(cls, prefix, path, term_set):
        if not path.startswith(prefix):
            return False

        return Term.suffix(prefix, path) in term_set


    # ----------------------------------------------------------------------------------------------------------------

    __CATALOGUE_NAME = 'compendia'

    @classmethod
    def catalogue_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), cls.__CATALOGUE_NAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, is_error_model, data_set, recs, device_prefix, primary_values, secondary_values, output_path,
                  outputs, reference_prefix, target_path, reference_targets, reference_environments):
        period = TrainingPeriod.construct(recs)

        primaries = {Term.suffix(device_prefix, path): PrimaryTerm.construct(path, values, prec=3)
                     for path, values in primary_values.items()}

        secondaries = {Term.suffix(device_prefix, path): SecondaryTerm.construct(path, values, prec=3)
                       for path, values in secondary_values.items()}

        reference = ReferenceCompendium.construct(reference_prefix, target_path, reference_targets,
                                                  reference_environments)

        output = Term.construct(output_path, outputs, prec=1)

        performance = LinRegress.construct(reference_targets, outputs, prec=3)

        return cls(is_error_model, data_set, period, primaries, secondaries, reference, output, performance)


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        is_error_model = jdict.get('is-error-model', False)
        data_set = jdict.get('data-set')
        period = TrainingPeriod.construct_from_jdict(jdict.get('period'))

        primaries = {path: PrimaryTerm.construct_from_jdict(term_jdict)
                     for path, term_jdict in jdict.get('primaries').items()}

        secondaries = {path: SecondaryTerm.construct_from_jdict(term_jdict)
                       for path, term_jdict in jdict.get('secondaries').items()}

        reference = Term.construct_from_jdict(jdict.get('reference'))

        output = Term.construct_from_jdict(jdict.get('output'))

        performance = LinRegress.construct_from_jdict(jdict.get('performance'))

        return cls(is_error_model, data_set, period, primaries, secondaries, reference, output, performance)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, is_error_model, data_set, period, primaries, secondaries, reference, output, performance):
        """
        Constructor
        """
        self.__is_error_model = bool(is_error_model)        # bool
        self.__data_set = data_set                          # string
        self.__period = period                              # TrainingPeriod

        self.__primaries = primaries                        # dict of path: PrimaryTerm
        self.__secondaries = secondaries                    # dict of path: SecondaryTerm
        self.__reference = reference                        # ReferenceCompendium
        self.__output = output                              # Term

        self.__performance = performance                    # LinRegress

        self.__logger = Logging.getLogger()


    def __len__(self):
        return len(self.performance)


    # ----------------------------------------------------------------------------------------------------------------

    def is_in_bounds(self, datum: PathDict):
        for datum_path in datum.paths():
            if datum_path in self.secondaries:
                if not self.secondaries[datum_path].is_in_bounds(datum.node(datum_path)):
                    return False

        return True


    def postprocess(self, model_output):
        # self.__logger.info("postprocess - primary_path: %s vcal_excess: %s model_output: %s" %
        #                    (primary_path, vcal_excess, model_output))

        corrected_exg = (model_output - self.performance.intercept) / self.performance.slope

        return corrected_exg


    # ----------------------------------------------------------------------------------------------------------------

    def primary_paths(self):
        return [primary.path for primary in self.primaries.values()]


    def primary_term(self, path):
        try:
            return self.primaries[path]
        except KeyError:
            return None


    def secondary_paths(self):
        return [secondary.path for secondary in self.secondaries.values()]


    def secondary_term(self, path):
        try:
            return self.secondaries[path]
        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        pieces = self.output.path.split('.')
        return '.'.join(pieces[1:])


    @property
    def species_name(self):
        pieces = self.output.path.split('.')
        return pieces[1]


    @property
    def model_name(self):
        pieces = self.output.path.split('.')
        return pieces[2]


    @property
    def device_name(self):
        pieces = self.output.path.split('.')
        return pieces[3]


    @property
    def period_name(self):
        pieces = self.output.path.split('.')
        return pieces[4]


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_error_model(self):
        return self.__is_error_model


    @property
    def data_set(self):
        return self.__data_set


    @property
    def period(self):
        return self.__period


    @property
    def primaries(self):
        return self.__primaries


    @property
    def secondaries(self):
        return self.__secondaries


    @property
    def reference(self):
        return self.__reference


    @property
    def output(self):
        return self.__output


    @property
    def performance(self):
        return self.__performance


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['is-error-model'] = self.is_error_model
        jdict['data-set'] = self.data_set
        jdict['period'] = self.period

        jdict['primaries'] = self.primaries
        jdict['secondaries'] = self.secondaries
        jdict['reference'] = self.reference
        jdict['output'] = self.output

        jdict['performance'] = self.performance

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        primaries = Str.collection(self.primaries)
        secondaries = Str.collection(self.secondaries)

        return "ModelCompendium:{name:%s, is_error_model:%s, data_set:%s, period:%s, primaries:%s, secondaries:%s, " \
               "reference:%s, output:%s, performance:%s}" %  \
               (self.name, self.is_error_model, self.data_set, self.period, primaries, secondaries,
                self.reference, self.output, self.performance)
