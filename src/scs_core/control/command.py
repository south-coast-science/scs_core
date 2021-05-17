"""
Created on 11 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://pymotw.com/2/subprocess/
"""

import os

from collections import OrderedDict
from subprocess import Popen, PIPE, TimeoutExpired

from scs_core.data.json import JSONable, JSONify


# --------------------------------------------------------------------------------------------------------------------

class Command(JSONable):
    """
    classdocs
    """

    __LIST_CMD = '?'

    __PROHIBITED_TOKENS = ('-i', '--interactive', '<', '>', ';', '|')

    __DEFAULT_TIMEOUT = 30.0            # seconds


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

        datum = cls(cmd, params, stdout=stdout, stderr=stderr, return_code=return_code)

        return datum


    @classmethod
    def construct_from_tokens(cls, tokens):
        if not tokens:
            return cls(None, [])

        cmd = tokens[0]
        params = tokens[1:]

        return cls(cmd, params)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cmd, params, stdout=None, stderr=None, return_code=None):
        """
        Constructor
        """
        self.__cmd = cmd                        # string
        self.__params = params                  # array

        self.__stdout = stdout                  # array of string
        self.__stderr = stderr                  # array of string
        self.__return_code = return_code        # int


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self, host):
        try:
            host.command_path()
        except NotImplementedError:
            return False

        if set(self.params).intersection(set(Command.__PROHIBITED_TOKENS)):
            return False

        if self.cmd == Command.__LIST_CMD:
            return True

        if self.cmd not in os.listdir(host.command_path()):
            return False

        return True


    def execute(self, host, timeout):
        if not self.cmd:
            return None

        try:
            if self.cmd == Command.__LIST_CMD:
                result = self.__execute('ls', host, timeout)

                self.__stdout = [JSONify.dumps(self.__stdout)]

            else:
                statement = ['./' + self.cmd]
                statement.extend(self.params)

                result = self.__execute(statement, host, timeout)

        except OSError as ex:
            return self.error(repr(ex))

        return result


    def error(self, message):
        self.__stdout = []
        self.__stderr = [message]
        self.__return_code = 1


    # ----------------------------------------------------------------------------------------------------------------

    def __execute(self, statement, host, timeout):
        p = Popen(statement, cwd=host.command_path(), stdout=PIPE, stderr=PIPE)

        try:
            stdout_bytes, stderr_bytes = p.communicate(timeout=timeout)

            self.__stdout = stdout_bytes.decode().strip().splitlines()
            self.__stderr = stderr_bytes.decode().strip().splitlines()
            self.__return_code = p.returncode

            return self.__return_code == 0

        except TimeoutExpired as ex:
            self.error(repr(ex))
            return False


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
