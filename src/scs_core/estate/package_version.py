"""
Created on 3 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/6677424/how-do-i-import-variable-packages-in-python-like-using-variable-variables-i

example JSON:
{"scs_core": {"repo": "scs_core", "version": "1.0.5"}, "scs_dev": {"repo": "scs_dev", "version": "1.0.4"},
"scs_dfe": {"repo": "scs_dfe_eng", "version": "1.0.2"}, "scs_host": {"repo": "scs_host_cpc", "version": "1.0.2"},
"scs_inference": {"repo": "scs_inference", "version": null}, "scs_mfr": {"repo": "scs_mfr", "version": "1.0.2"},
"scs_ndir": {"repo": "scs_ndir", "version": "0.9.1"}, "scs_psu": {"repo": "scs_psu", "version": "1.0.5"}}
"""

import os

from collections import OrderedDict
from importlib import import_module

from scs_core.data.json import JSONable, MultiPersistentJSONable
from scs_core.data.str import Str

from scs_core.estate.git_pull import GitPull

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class PackageVersion(MultiPersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "package_version.json"

    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))

        return cls.conf_dir(), filename


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_installation(cls, package, repository):
        try:
            module = import_module(package)
        except ModuleNotFoundError:
            return cls(package, repository, None)

        try:
            # noinspection PyUnresolvedReferences
            version = module.__version__
        except AttributeError:
            version = None

        return cls(package, repository, version)


    @classmethod
    def construct_from_jdict(cls, jdict, name=None, skeleton=False):
        if not jdict:
            return None

        repository = jdict.get('repo')
        version = jdict.get('version')

        return cls(name, repository, version)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, repository, version):
        """
        Constructor
        """
        super().__init__(name)

        self.__repository = repository              # string
        self.__version = version                    # string


    def __eq__(self, other):
        try:
            return self.repository == other.repository and self.version == other.version
        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def repository(self):
        return self.__repository


    @property
    def version(self):
        return self.__version


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['repo'] = self.repository
        jdict['version'] = self.version

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PackageVersion:{name:%s, repository:%s, version:%s}" %  (self.name, self.repository, self.version)


# --------------------------------------------------------------------------------------------------------------------

class PackageVersions(JSONable):
    """
    classdocs
    """

    __GREENGRASS_PACKAGE = 'scs_greengrass'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_installation(cls, root, manager):
        versions = {}

        # local...
        for repository in GitPull.dirs(root):
            contents = Filesystem.ls(os.path.join(root, repository, 'src'))

            for content in contents:
                package = content.name
                versions[package] = PackageVersion.construct_from_installation(package, repository)

        # greengrass...
        greengrass_version = PackageVersion.load(manager, name=cls.__GREENGRASS_PACKAGE)

        if greengrass_version is not None:
            versions[cls.__GREENGRASS_PACKAGE] = greengrass_version

        return cls(versions)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if jdict is None:
            return None

        versions = {}

        for package, version in jdict.items():
            versions[package] = PackageVersion.construct_from_jdict(version, name=package)

        return cls(versions)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, versions):
        """
        Constructor
        """
        self.__versions = versions                  # dict of package: PackageVersion


    def __len__(self):
        return len(self.versions)


    def __eq__(self, other):
        try:
            if len(self) != len(other):
                return False

            for package in self.__versions.keys():
                if self.__versions[package] != other.__versions[package]:
                    return False

            return True

        except (KeyError, TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def version(self, package):
        try:
            return self.__versions[package]

        except KeyError:
            return None


    @property
    def versions(self):
        return {package: self.__versions[package] for package in sorted(self.__versions.keys())}


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.versions


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PackageVersions:{versions:%s}" %  Str.collection(self.versions)
