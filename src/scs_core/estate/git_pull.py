"""
Created on 24 Feb 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

JSON example:
"""

from collections import OrderedDict
from subprocess import Popen, PIPE, TimeoutExpired

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import PersistentJSONable

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class GitPull(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "git_pull.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    @classmethod
    def construct_from_jdict(cls, jdict, default=True):
        if not jdict:
            return None if default is None else cls(None, False, [], [])

        pulled_on = LocalizedDatetime.construct_from_jdict(jdict.get('pulled-on'))
        success = jdict.get('success')
        installed = jdict.get('installed')
        updated = jdict.get('updated')

        return cls(pulled_on, success, installed, updated)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def dirs(cls, root):
        return [item.name for item in Filesystem.ls(root) if item.name.startswith("scs_")]


    @classmethod
    def is_clone(cls, path):
        return '.git' in [item.name for item in Filesystem.ls(path)]


    @classmethod
    def pull_repo(cls, path, timeout):
        try:
            p = Popen(['git', '-C', path, 'pull'], stdout=PIPE, stderr=PIPE)
            stdout_bytes, stderr_bytes = p.communicate(None, timeout)

            success = p.returncode == 0
            stdout = stdout_bytes.decode()
            stderr = stderr_bytes.decode()

            return success, stdout, stderr

        except TimeoutExpired:
            raise TimeoutError(timeout)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pulled_on, success, installed, updated):
        """
        Constructor
        """
        self.__pulled_on = pulled_on                    # LocalizedDatetime
        self.__success = success                        # bool
        self.__installed = installed                    # array of strings
        self.__updated = updated                        # array of strings


    # ----------------------------------------------------------------------------------------------------------------

    def is_comprehensive(self):
        return self.installed == self.updated


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['pulled-on'] = None if self.pulled_on is None else self.pulled_on.as_iso8601()
        jdict['success'] = self.success
        jdict['installed'] = self.installed
        jdict['updated'] = self.updated

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pulled_on(self):
        return self.__pulled_on


    @property
    def success(self):
        return self.__success


    @property
    def installed(self):
        return self.__installed


    @property
    def updated(self):
        return self.__updated


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GitPull:{pulled_on:%s, success:%s, installed:%s, updated:%s}" % \
               (self.pulled_on, self.success, self.installed, self.updated)
