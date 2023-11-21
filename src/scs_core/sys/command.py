"""
Created on 15 Sep 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://pymotw.com/2/subprocess/
"""

import json
import sys

from subprocess import Popen, PIPE

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class JSONPopen(Popen):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    #     def __init__(self, args, bufsize=-1, executable=None,
    #                  stdin=None, stdout=None, stderr=None,
    #                  preexec_fn=None, close_fds=True,
    #                  shell=False, cwd=None, env=None, universal_newlines=None,
    #                  startupinfo=None, creationflags=0,
    #                  restore_signals=True, start_new_session=False,
    #                  pass_fds=(), *, encoding=None, errors=None, text=None):
    def __init__(self, args, bufsize=-1, executable=None,
                 stdin=None, stdout=None, stderr=None,
                 preexec_fn=None, close_fds=True,
                 shell=False, cwd=None, env=None, universal_newlines=None,
                 startupinfo=None, creationflags=0,
                 restore_signals=True, start_new_session=False,
                 pass_fds=(), encoding=None, errors=None, text=None):
        """
        Constructor
        """
        super().__init__(args, bufsize=bufsize, executable=executable,
                         stdin=stdin, stdout=stdout, stderr=stderr,
                         preexec_fn=preexec_fn, close_fds=close_fds,
                         shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                         startupinfo=startupinfo, creationflags=creationflags,
                         restore_signals=restore_signals, start_new_session=start_new_session,
                         pass_fds=pass_fds, encoding=encoding, errors=errors, text=text)


    # ----------------------------------------------------------------------------------------------------------------

    def json(self):
        return json.loads(self.stdout.readline().decode())


    def json_lines(self):
        for line in self.stdout.readlines():
            yield json.loads(line.decode())


# --------------------------------------------------------------------------------------------------------------------

class Command(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose, on_abort=None):
        """
        Constructor
        """
        self.__verbose = verbose                            # bool
        self.__on_abort = on_abort                          # function

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def s(self, cmd_args, wait=True, no_verbose=False, abort_on_fail=True):
        tokens = self.__cmd(cmd_args, no_verbose=no_verbose)
        p = JSONPopen(' '.join(tokens), shell=True)

        return self.__process(p, wait=wait, abort_on_fail=abort_on_fail)


    def o(self, cmd_args, wait=False, no_verbose=False, abort_on_fail=True):
        tokens = self.__cmd(cmd_args, no_verbose=no_verbose)
        p = JSONPopen(tokens, stdout=PIPE)

        return self.__process(p, wait=wait, abort_on_fail=abort_on_fail)


    def io(self, p: JSONPopen, cmd_args, wait=False, no_verbose=False, abort_on_fail=True):
        tokens = self.__cmd(cmd_args, no_verbose=no_verbose)
        p = JSONPopen(tokens, stdin=p.stdout, stdout=PIPE)

        return self.__process(p, wait=wait, abort_on_fail=abort_on_fail)


    def i(self, p: JSONPopen, cmd_args, wait=True, no_verbose=False, abort_on_fail=True):
        tokens = self.__cmd(cmd_args, no_verbose=no_verbose)
        p = JSONPopen(tokens, stdin=p.stdout, stdout=sys.stderr)

        return self.__process(p, wait=wait, abort_on_fail=abort_on_fail)


    # ----------------------------------------------------------------------------------------------------------------

    def __cmd(self, cmd_args, no_verbose=False):
        tokens = [str(cmd_arg) for cmd_arg in cmd_args if cmd_arg is not None]

        if self.__verbose and not no_verbose:
            tokens = tokens[:1] + ['-v'] + tokens[1:]

        self.__logger.info(' '.join(tokens))

        return tokens


    def __process(self, p: JSONPopen, wait=False, abort_on_fail=True):
        if wait:
            p.wait()

        if abort_on_fail and (p.returncode is not None and p.returncode != 0):
            self.abort(p.returncode)

        return p


    def abort(self, return_code):
        self.__logger.error('ABORTED.')

        if self.__on_abort:
            self.__on_abort()

        exit(return_code)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Command:{verbose:%s, on_abort:%s}" % (self.verbose, self.__on_abort)
