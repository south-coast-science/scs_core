"""
Created on 1 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_analysis
"""

import sys

from decimal import InvalidOperation

from scs_core.data.categorical_regression import CategoricalRegression
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONify
from scs_core.data.linear_regression import LinearRegression
from scs_core.data.path_dict import PathDict
from scs_core.data.precision import Precision


# --------------------------------------------------------------------------------------------------------------------

class Aggregate(object):
    """
    classdocs
    """

    RULE_RATIO = 0.75                                   # ratio of reported points to expected points - 75%

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, min_max, iso_path, nodes):
        """
        Constructor
        """
        self.__min_max = min_max                        # bool
        self.__iso_path = iso_path                      # string
        self.__nodes = nodes                            # list of string

        self.__precisions = {}                          # dict of path: Precision
        self.__regressions = {}                         # dict of path: LinearRegression

        self.__initialised = False                      # bool
        self.__block_sample_count = 0                   # int


    # ----------------------------------------------------------------------------------------------------------------

    def has_value(self):
        for regression in self.__regressions.values():
            if regression.has_midpoint():
                return True

        return False


    def append(self, datetime: LocalizedDatetime, sample: PathDict):
        # initialise...
        if not self.__initialised:
            nodes = self.__nodes if self.__nodes else sample.paths()        # use all paths if nodes are not specified

            for node in nodes:
                try:
                    paths = sample.paths(node)
                except KeyError:
                    continue

                except IndexError as ex:
                    paths = None
                    print("sample_aggregate: %s: IndexError: %s" % (node, ex), file=sys.stderr)
                    sys.stderr.flush()
                    exit(1)

                for path in paths:
                    if path == 'rec':
                        continue

                    self.__precisions[path] = Precision()
                    self.__regressions[path] = LinearRegression() if Datum.is_numeric(sample.node(path)) else \
                        CategoricalRegression()

            self.__initialised = True

        # values...
        for path in self.__precisions.keys():
            try:
                value = sample.node(path)
            except KeyError:
                continue

            if value is None:
                continue

            try:
                self.__precisions[path].widen(value)
                self.__regressions[path].append(datetime, value)
            except InvalidOperation:
                continue

        self.__block_sample_count += 1


    def reset(self):
        self.__block_sample_count = 0

        for path in self.__regressions.keys():
            self.__regressions[path].reset()


    def report(self, localised_datetime):
        report = PathDict()

        # rec...
        report.append(self.__iso_path, localised_datetime.as_iso8601())

        # values...
        for path, precision in self.__precisions.items():
            regression = self.__regressions[path]

            if self.__regressions[path].has_midpoint():
                _, midpoint = regression.midpoint(precision.digits)

                if self.__min_max:
                    report.append(path + '.min', regression.min(precision.digits))
                    report.append(path + '.mid', midpoint)
                    report.append(path + '.max', regression.max(precision.digits))

                else:
                    report.append(path, midpoint)

        return report


    def print(self, localised_datetime):
        print(JSONify.dumps(self.report(localised_datetime)))
        sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------

    def complies_with_rule(self, sampling_interval, aggregate_interval):
        expected_count = aggregate_interval.total_seconds() / sampling_interval.total_seconds()
        ratio = self.block_sample_count / expected_count

        return ratio >= self.RULE_RATIO


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def block_sample_count(self):
        return self.__block_sample_count


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        regressions = '{' + ', '.join(topic + ': ' + str(reg) for topic, reg in self.__regressions.items()) + '}'

        return "Aggregate:{min_max:%s, iso_path:%s block_sample_count:%s, regressions:%s}" % \
               (self.__min_max, self.__iso_path, self.block_sample_count, regressions)
