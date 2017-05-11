"""
Created on 11 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://pymotw.com/2/subprocess/
"""

import os
import subprocess

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Command(JSONable):
    """
    classdocs
    """

    __PROHIBITED_TOKENS = ('<', '>', ';', '|')

    __TIMEOUT = 60.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        cmd = jdict.get('cmd')
        params = jdict.get('params')

        stdout = jdict.get('stdout')
        stderr = jdict.get('stderr')
        return_code = jdict.get('ret')

        datum = Command(cmd, params, stdout, stderr, return_code)

        return datum


    @classmethod
    def construct_from_tokens(cls, tokens):
        if not tokens:
            return Command(None, [])

        cmd = tokens[0]
        params = tokens[1:]

        return Command(cmd, params)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cmd, params, stdout=None, stderr=None, return_code=None):
        """
        Constructor
        """
        self.__cmd = cmd                        # string
        self.__params = params                  # array

        self.__stdout = stdout                  # array
        self.__stderr = stderr                  # array
        self.__return_code = return_code        # int


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self, host):
        try:
            host.COMMAND_DIR
        except AttributeError:
            return False

        if set(self.params).intersection(set(Command.__PROHIBITED_TOKENS)):
            return False

        if self.cmd not in os.listdir(host.COMMAND_DIR):
            return False

        return True


    def execute(self, host):
        if not self.cmd:
            return

        statement = ['./' + self.cmd]
        statement.extend(self.params)

        proc = subprocess.Popen(statement, cwd=host.COMMAND_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout_bytes, stderr_bytes = proc.communicate(None, Command.__TIMEOUT)

        self.__stdout = stdout_bytes.decode().strip().splitlines()
        self.__stderr = stderr_bytes.decode().strip().splitlines()
        self.__return_code = proc.returncode

        return self.__return_code == 0


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['cmd'] = self.cmd
        jdict['params'] = self.params

        jdict['stdout'] = self.stdout
        jdict['stderr'] = self.stderr
        jdict['ret'] = self.return_code

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cmd(self):
        return self.__cmd


    @property
    def params(self):
        return self.__params


    @property
    def stdout(self):
        return self.__stdout


    @property
    def stderr(self):
        return self.__stderr


    @property
    def return_code(self):
        return self.__return_code


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Command:{cmd:%s, params:%s, stdout:%s, stderr:%s, return_code:%s}" % \
               (self.cmd, self.params, self.stdout, self.stderr, self.return_code)
