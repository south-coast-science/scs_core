"""
Created on 12 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import shutil


# TODO: use the Filesystem.mkdir(..) method to auto-create conf directories, etc.

# --------------------------------------------------------------------------------------------------------------------

class Filesystem(object):

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def mkdir(cls, path):
        if not path or os.path.exists(path):
            return

        head, _ = os.path.split(path)

        if head and not os.path.exists(head):
            cls.mkdir(head)

        os.mkdir(path)


    @classmethod
    def rmdir(cls, path):
        if not path or not os.path.exists(path):
            return

        shutil.rmtree(path)
