"""
Created on 6 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: Methods

NB: initialisation is performed at the foot of this class

example:
{"Parameter": "Oxides of nitrogen (NOx)", "Parameter Code": 42603, "Method Code": 31, "Recording Mode": "Continuous",
"Collection Description": "INSTRUMENTAL", "Analysis Description": "CHEMILUMINESCENCE", "Method Type": "FRM",
"Reference Method ID": "RFNA-1078-031", "Equivalent Method": "MELOY NA530R", "Federal MDL": "10",
"Min Value": "-5", "Max Value": "1200", "Digits": "1", "Round Truncate Indicator": "T",
"Units": "Parts per billion"}

suspect rows:
Outdoor Temperature,62101,59,Continuous,Instrumental,Vaisala HMP 155,,,,-60,,,1,R,Degrees Fahrenheit
Outdoor Temperature,62101,59,Continuous,Instrumental,Vaisala HMP 155,,,,-60,,,1,R,Degrees Fahrenheit

https://www.airnow.gov/
"""

import os

from collections import OrderedDict

from scs_core.csv.csv_archive import CSVArchive

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Method(CSVArchive, JSONable):
    """
    classdocs
    """

    _retrieved = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def archive_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'archive', 'methods.csv')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def find_by_parameter_code(cls, parameter_code):
        for method in cls._retrieved.values():
            if method.parameter_code == parameter_code:
                yield method


    @classmethod
    def find_by_method_code(cls, method_code):
        for method in cls._retrieved.values():
            if method.method_code == method_code:
                yield method


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        parameter = jdict.get('Parameter')
        parameter_code = jdict.get('Parameter Code')
        method_code = jdict.get('Method Code')
        recording_mode = jdict.get('Recording Mode')

        collection_description = jdict.get('Collection Description')
        analysis_description = jdict.get('Analysis Description')

        method_type = jdict.get('Method Type')
        reference_method_id = jdict.get('Reference Method ID')
        equivalent_method = jdict.get('Equivalent Method')

        federal_mdl = jdict.get('Federal MDL')

        min_value = jdict.get('Min Value')
        max_value = jdict.get('Max Value')
        digits = jdict.get('Digits')

        round_truncate_indicator = jdict.get('Round Truncate Indicator')
        units = jdict.get('Units')

        return Method(parameter, parameter_code, method_code, recording_mode,
                      collection_description, analysis_description, method_type, reference_method_id, equivalent_method,
                      federal_mdl, min_value, max_value, digits, round_truncate_indicator, units)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, parameter, parameter_code, method_code, recording_mode,
                 collection_description, analysis_description, method_type, reference_method_id, equivalent_method,
                 federal_mdl, min_value, max_value, digits, round_truncate_indicator, units):
        """
        Constructor
        """
        self.__parameter = parameter                                        # string
        self.__parameter_code = int(parameter_code)                         # int(5)
        self.__method_code = int(method_code)                               # int(3)
        self.__recording_mode = recording_mode                              # string

        self.__collection_description = collection_description              # string
        self.__analysis_description = analysis_description                  # string
        self.__method_type = method_type                                    # string
        self.__reference_method_id = reference_method_id                    # string
        self.__equivalent_method = equivalent_method                        # string

        self.__federal_mdl = Datum.float(federal_mdl)                       # float
        self.__min_value = Datum.float(min_value)                           # float
        self.__max_value = Datum.float(max_value)                           # float
        self.__digits = Datum.int(digits)                                   # int

        self.__round_truncate_indicator = round_truncate_indicator          # string
        self.__units = units                                                # string


    def __eq__(self, other):
        try:
            return self.parameter == other.parameter and \
                   self.parameter_code == other.parameter_code and \
                   self.method_code == other.method_code and \
                   self.recording_mode == other.recording_mode and \
                   self.collection_description == other.collection_description and \
                   self.analysis_description == other.analysis_description and \
                   self.method_type == other.method_type and \
                   self.reference_method_id == other.reference_method_id and \
                   self.equivalent_method == other.equivalent_method and \
                   self.federal_mdl == other.federal_mdl and \
                   self.min_value == other.min_value and \
                   self.max_value == other.max_value and \
                   self.digits == other.digits and \
                   self.round_truncate_indicator == other.round_truncate_indicator and \
                   self.units == other.units

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['Parameter'] = self.parameter
        jdict['Parameter Code'] = self.parameter_code
        jdict['Method Code'] = self.method_code
        jdict['Recording Mode'] = self.recording_mode

        jdict['Collection Description'] = self.collection_description
        jdict['Analysis Description'] = self.analysis_description
        jdict['Method Type'] = self.method_type
        jdict['Reference Method ID'] = self.reference_method_id
        jdict['Equivalent Method'] = self.equivalent_method

        jdict['Federal MDL'] = self.federal_mdl
        jdict['Min Value'] = self.min_value
        jdict['Max Value'] = self.max_value
        jdict['Digits'] = self.digits

        jdict['Round Truncate Indicator'] = self.round_truncate_indicator
        jdict['Units'] = self.units

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pk(self):
        return self.parameter_code, self.method_code


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def parameter(self):
        return self.__parameter


    @property
    def parameter_code(self):
        return self.__parameter_code


    @property
    def method_code(self):
        return self.__method_code


    @property
    def recording_mode(self):
        return self.__recording_mode


    @property
    def collection_description(self):
        return self.__collection_description


    @property
    def analysis_description(self):
        return self.__analysis_description


    @property
    def method_type(self):
        return self.__method_type


    @property
    def reference_method_id(self):
        return self.__reference_method_id


    @property
    def equivalent_method(self):
        return self.__equivalent_method


    @property
    def federal_mdl(self):
        return self.__federal_mdl


    @property
    def min_value(self):
        return self.__min_value


    @property
    def max_value(self):
        return self.__max_value


    @property
    def digits(self):
        return self.__digits


    @property
    def round_truncate_indicator(self):
        return self.__round_truncate_indicator


    @property
    def units(self):
        return self.__units


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Method:{parameter:%s, parameter_code:%05d, method_code:%03d, recording_mode:%s, " \
               "collection_description:%s, analysis_description:%s, method_type:%s, reference_method_id:%s, " \
               "equivalent_method:%s, federal_mdl:%s, min_value:%s, max_value:%s, digits:%s, " \
               "round_truncate_indicator:%s, units:%s}" % \
               (self.parameter, self.parameter_code, self.method_code, self.recording_mode,
                self.collection_description, self.analysis_description, self.method_type, self.reference_method_id,
                self.equivalent_method, self.federal_mdl, self.min_value, self.max_value, self.digits,
                self.round_truncate_indicator, self.units)


# --------------------------------------------------------------------------------------------------------------------
# initialisation...

Method.retrieve()
