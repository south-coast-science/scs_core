"""
Created on 13 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command example:
ps -Ao ppid,pid,uid,tty,pmem,pcpu,cputime,etime,args -w -w

report examples:
  154 26605   502 ??        0.0   0.0   0:00.37 01-00:43:12 /usr/bin/ssh-agent -l
  154 39364   502 ??        6.3  31.5  22:58.40    02:26:25 /Applications/PyCharm.app/Contents/MacOS/pycharm

JSON example:
{"ppid": 154, "pid": 26605, "uid": 502, "tty": "??", "pcpu": 0.0, "pmem": 0.0,
"cpu": {"days": 0, "hours": 0, "minutes": 0, "seconds": 0, "millis": 370},
"elapsed": {"days": 1, "hours": 0, "minutes": 43, "seconds": 12, "millis": 0},
"cmd": "/usr/bin/ssh-agent -l"}
"""

import re

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class PsDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_report(cls, report):
        mat = re.match(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\S+)\s+(\S+)\s+(.+)$',
                       report)

        if mat is None:
            return None

        fields = mat.groups()

        ppid = int(fields[0])
        pid = int(fields[1])
        uid = int(fields[2])
        tty = fields[3]

        pcpu = float(fields[4])
        pmem = float(fields[5])

        cpu_time = Timedelta.construct_from_ps_time_report(fields[6])
        elapsed_time = Timedelta.construct_from_ps_elapsed_report(fields[7])
        cmd = fields[8]

        return PsDatum(ppid, pid, uid, tty, pcpu, pmem, cpu_time, elapsed_time, cmd)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        ppid = int(jdict.get('ppid'))
        pid = int(jdict.get('pid'))
        uid = int(jdict.get('uid'))
        tty = jdict.get('tty')

        pcpu = float(jdict.get('pcpu'))
        pmem = float(jdict.get('pmem'))

        cpu_time = Timedelta.construct_from_jdict(jdict.get('cpu'))
        elapsed_time = Timedelta.construct_from_jdict(jdict.get('elapsed'))

        cmd = jdict.get('cmd')

        return PsDatum(ppid, pid, uid, tty, pcpu, pmem, cpu_time, elapsed_time, cmd)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ppid, pid, uid, tty, pcpu, pmem, cpu_time, elapsed_time, cmd):
        """
        Constructor
        """
        self.__ppid = ppid                  # int               parent process ID
        self.__pid = pid                    # int               process ID
        self.__uid = uid                    # int               user ID
        self.__tty = tty                    # string            TTY

        self.__pcpu = pcpu                  # float             % CPU
        self.__pmem = pmem                  # float             % memory

        self.__cpu_time = cpu_time          # Timedelta
        self.__elapsed_time = elapsed_time  # Timedelta

        self.__cmd = cmd                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['ppid'] = self.ppid
        jdict['pid'] = self.pid
        jdict['uid'] = self.uid
        jdict['tty'] = self.tty

        jdict['pcpu'] = self.pcpu
        jdict['pmem'] = self.pmem

        jdict['cpu'] = self.cpu_time
        jdict['elapsed'] = self.elapsed_time

        jdict['cmd'] = self.cmd

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def ppid(self):
        return self.__ppid


    @property
    def pid(self):
        return self.__pid


    @property
    def uid(self):
        return self.__uid


    @property
    def tty(self):
        return self.__tty


    @property
    def pcpu(self):
        return self.__pcpu


    @property
    def pmem(self):
        return self.__pmem


    @property
    def cpu_time(self):
        return self.__cpu_time


    @property
    def elapsed_time(self):
        return self.__elapsed_time


    @property
    def cmd(self):
        return self.__cmd


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PsDatum:{ppid:%s, pid:%s, uid:%s, tty:%s, pcpu:%s, pmem:%s, " \
               "cpu_time:%s, elapsed_time:%s, cmd:%s}" %  \
               (self.ppid, self.pid, self.uid, self.tty, self.pcpu, self.pmem,
                self.cpu_time, self.elapsed_time, self.cmd)
