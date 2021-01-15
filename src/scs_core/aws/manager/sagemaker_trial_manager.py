"""
Created on 04 Dec 2020

@author: Jade Page (jade.page@southcoastscience.com)

"""

import sys


# --------------------------------------------------------------------------------------------------------------------

class SagemakerTrialManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client):
        """
        Constructor
        """
        self.__client = client


    # ----------------------------------------------------------------------------------------------------------------

    def list_experiments(self, time_order):
        names = []
        next_token = None

        try:
            while True:
                res, next_token = self.retrieve_experiments(time_order, next_token)
                experiments = res.get("ExperimentSummaries")

                for item in experiments:
                    name = item.get("ExperimentName")
                    names.append(name)

                if not next_token:
                    return names

        except self.__client.exceptions.ResourceNotFound:
            print("Resource not found - ensure your auth is for the correct account", file=sys.stderr)


    def retrieve_experiments(self, time_order, next_token):
        next_token2 = None

        if next_token:
            response = self.__client.list_experiments(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
            )
        else:
            response = self.__client.list_experiments(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
            )

        if "NextToken" in response:
            next_token2 = response.get("NextToken")

        return response, next_token2


    def list_components(self, experiment_string, trial_string, time_order):
        components = []
        next_token = None

        try:
            if trial_string:
                while True:
                    res, next_token = self.retrieve_trial_components(trial_string, time_order, next_token)
                    components.append(res)

                    if not next_token:
                        return components

            elif experiment_string:
                while True:
                    res, next_token = self.retrieve_experiment_components(experiment_string, time_order, next_token)
                    components.append(res)

                    if not next_token:
                        return components

        except self.__client.exceptions.ResourceNotFound:
            print("Resource not found - please check the filter string", file=sys.stderr)


    def retrieve_trial_components(self, trial_string, time_order, next_token):
        next_token2 = None

        if next_token:
            response = self.__client.list_trial_components(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
                TrialName=trial_string,
                NextToken=next_token
            )
        else:
            response = self.__client.list_trial_components(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
                TrialName=trial_string
            )

        if "NextToken" in response:
            next_token2 = response.get("NextToken")

        return response, next_token2


    def retrieve_experiment_components(self, experiment_string, time_order, next_token):
        next_token2 = None

        if next_token:
            response = self.__client.list_trial_components(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
                ExperimentName=experiment_string,
                NextToken=next_token
            )
        else:
            response = self.__client.list_trial_components(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
                ExperimentName=experiment_string
            )

        if "NextToken" in response:
            next_token2 = response.get("NextToken")

        return response, next_token2


    def list_trial_names_filter(self, experiment_string, time_order):
        names = []
        next_token = None

        try:
            while True:
                res, next_token = self.retrieve_filtered_trials(experiment_string, time_order, next_token)
                models = res.get("TrialSummaries")

                for item in models:
                    name = item.get("TrialName")
                    names.append(name)

                if not next_token:
                    return names

        except self.__client.exceptions.ResourceNotFound:
            print("Resource not found - please check the filter string", file=sys.stderr)


    def list_trial_names(self, time_order):
        names = []
        next_token = None

        try:
            while True:
                res, next_token = self.retrieve_trials(time_order, next_token)
                models = res.get("TrialSummaries")

                for item in models:
                    name = item.get("TrialName")
                    names.append(name)

                if not next_token:
                    return names

        except self.__client.exceptions.ResourceNotFound:
            print("Resource not found - ensure your auth is for the correct account", file=sys.stderr)


    def retrieve_trials(self, time_order, next_token=None):
        next_token2 = None

        if next_token:
            response = self.__client.list_trials(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
                NextToken=next_token
            )
        else:
            response = self.__client.list_trials(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100
            )

        if "NextToken" in response:
            next_token2 = response.get("NextToken")

        return response, next_token2


    def retrieve_filtered_trials(self, experiment_string, time_order, next_token=None):
        next_token2 = None

        if next_token:
            response = self.__client.list_trials(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
                ExperimentName=experiment_string,
                NextToken=next_token
            )
        else:
            response = self.__client.list_trials(
                SortBy='CreationTime' if time_order else 'Name',
                SortOrder='Descending' if time_order else 'Ascending',
                MaxResults=100,
                ExperimentName=experiment_string
            )

        if "NextToken" in response:
            next_token2 = response.get("NextToken")

        return response, next_token2


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SagemakerTrialManager:{client:%s}" % self.__client
