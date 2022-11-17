"""
Created on 19 Sep 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A catalogue entry for a machine learning model, for a specific gas

https://github.com/south-coast-science/scs_sagemaker_automl/blob/a1db0b830909b20fc3a7cea8b895a8bdb8d5b033/src/scs_sagemaker/project.py#L277

IMPORTANT: Assuming that the miniumum gas concentration in the data set is close to zero, the minimum vCal value
of the primary term indicates the minimum vCal value for every equivalent sensor - the vCal baseline on the target
devices should be set to make this so.

document example:
{"is-error-model": true,
"data-set": "ref-scs-bgx-642-gases-21Q3-slp16-clean-vcal-err",
"period": {"start": "2021-11-01T00:02:00Z", "end": "2021-12-28T06:57:00Z"},
"primaries": {"SO2.vCal": {"path": "src.scs.env.gases.val.SO2.vCal", "min": -355.462, "avg": 18.488, "max": 4256.394}},
"secondaries": {"tmp.brd": {"path": "src.scs.stat.val.tmp.brd", "min": 21.4, "avg": 31.994, "max": 48.7},
"hmd.cur": {"path": "src.scs.env.meteo.val.hmd.cur", "min": 11.0, "avg": 51.815, "max": 84.1},
"hmd.slope": {"path": "src.scs.env.meteo.val.hmd.slope", "min": -0.022, "avg": 0.0, "max": 0.031},
"tmp.cur": {"path": "src.scs.env.meteo.val.tmp.cur", "min": 16.3, "avg": 26.568, "max": 42.8},
"tmp.slope": {"path": "src.scs.env.meteo.val.tmp.slope", "min": -0.009, "avg": -0.0, "max": 0.003}},
"reference": {"path": "src.ref.gas.SO2", "min": 1.0, "avg": 18.5, "max": 3211.0},
"output": {"path": "exg.SO2.vE.Urban.21Q3", "min": -63.2, "avg": 18.6, "max": 4228.2},
"performance": {"count": 78052, "slope": 0.953, "intercept": 0.999, "r2": 0.863, "p": 0.0, "std-err": 0.001}}
"""

import os

from collections import OrderedDict

from scs_core.data.json import JSONCatalogueEntry, JSONify
from scs_core.data.lin_regress import LinRegress
from scs_core.data.path_dict import PathDict
from scs_core.data.str import Str

from scs_core.model.catalogue.term import Term, PrimaryTerm, SecondaryTerm
from scs_core.model.catalogue.training_period import TrainingPeriod

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class ModelCompendium(JSONCatalogueEntry):
    """
    classdocs
    """

    __CATALOGUE_NAME = 'compendia'

    @classmethod
    def catalogue_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), cls.__CATALOGUE_NAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __term_path(cls, path):
        return '.'.join(path.split('.')[-2:])


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, is_error_model, data_set, recs, primary_values, secondary_values, output_path, outputs,
                  reference_path, references):
        period = TrainingPeriod.construct(recs)

        primaries = {cls.__term_path(path): PrimaryTerm.construct(path, values, prec=3)
                     for path, values in primary_values.items()}

        secondaries = {cls.__term_path(path): SecondaryTerm.construct(path, values, prec=3)
                       for path, values in secondary_values.items()}

        reference = Term.construct(reference_path, references, prec=1)
        output = Term.construct(output_path, outputs, prec=1)

        performance = LinRegress.construct(references, outputs, prec=3)

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
        self.__reference = reference                        # Term
        self.__output = output                              # Term

        self.__performance = performance                    # LinRegress

        self.__logger = Logging.getLogger()


    def __len__(self):
        return len(self.performance)


    # ----------------------------------------------------------------------------------------------------------------

    def is_in_bounds(self, datum: PathDict):
        for datum_path in datum.paths():
            term_path = self.__term_path(datum_path)

            if term_path in self.secondaries:
                if not self.secondaries[term_path].is_in_bounds(datum.node(datum_path)):
                    return False

        return True


    def preprocess(self, datum: PathDict, offset=0, include_orig=False):
        target = PathDict()

        for datum_path in datum.paths():
            term_path = self.__term_path(datum_path)
            node = datum.node(datum_path)

            if term_path in self.primaries:
                value, extr = self.primaries[term_path].preprocess(node, offset)

                if include_orig:
                    target.append(datum_path + 'Orig', node)

                target.append(datum_path, None if value is None else "%g" % value)
                target.append(datum_path + 'Extr', None if value is None else "%g" % extr)
                continue

            if term_path in self.secondaries:
                value = self.secondaries[term_path].preprocess(node)

                if include_orig:
                    target.append(datum_path + 'Orig', node)

                target.append(datum_path, None if value is None else "%g" % value)
                continue

            target.append(datum_path, node)

        self.__logger.debug("preprocess - datum: %s" % JSONify.dumps(datum))
        self.__logger.debug("preprocess - target: %s" % JSONify.dumps(target))

        return target


    def postprocess(self, primary_path, vcal_excess, model_output):
        # self.__logger.info("postprocess - primary_path: %s vcal_excess: %s model_output: %s" %
        #                    (primary_path, vcal_excess, model_output))

        corrected_exg = (model_output - self.performance.intercept) / self.performance.slope

        # TODO: handle vCal and xCal excesses differently

        if vcal_excess > 0:
            model_vcal_max = self.primary_term(primary_path).maximum
            corrected_exg = corrected_exg * ((model_vcal_max + vcal_excess) / model_vcal_max)

        return corrected_exg


    # ----------------------------------------------------------------------------------------------------------------

    def primary_paths(self):
        return [primary.path for primary in self.primaries.values()]


    def primary_term(self, path):
        try:
            return self.primaries[self.__term_path(path)]
        except KeyError:
            return None


    def secondary_paths(self):
        return [secondary.path for secondary in self.secondaries.values()]


    def secondary_term(self, path):
        try:
            return self.secondaries[self.__term_path(path)]
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

    def as_json(self):
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
