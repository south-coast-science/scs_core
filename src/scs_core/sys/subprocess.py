"""
Created on 30 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from subprocess import check_output, Popen, PIPE

from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class Pipe(object):
    """
    classdocs
    """

    @staticmethod
    def __args(command):
        return [str(arg) for arg in command]


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *command):
        """
        Constructor
        """
        self.__commands = command               # array of arrays of scalar


    # ----------------------------------------------------------------------------------------------------------------

    def wait(self):
        if not self.__commands:
            return None

        count = len(self.__commands)

        p = None
        p_in = None

        for i in range(count):
            p_out = PIPE if i < count - 1 else None
            p = Popen(self.__args(self.__commands[i]), stdin=p_in, stdout=p_out)
            p_in = p.stdout

        p.wait()

        return p.returncode


    def check_output(self):
        if not self.__commands:
            return None

        count = len(self.__commands) - 1

        p_in = None

        for i in range(count):
            p = Popen(self.__args(self.__commands[i]), stdin=p_in, stdout=PIPE)
            p_in = p.stdout

        output = check_output(self.__args(self.__commands[count]), stdin=p_in)

        return output.decode().strip()


    # ----------------------------------------------------------------------------------------------------------------

    def as_script(self):
        script = ''

        for command in self.__commands:
            if script:
                script += ' | '

            for arg in self.__args(command):
                script += arg + ' '

        return script.strip()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Pipe:{commands:%s}" % Str.collection(self.__commands)
