#!/usr/bin/env python3

"""
Created on 19 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

def func():
    try:
        print("start")
        raise RuntimeError("TEST")

    finally:
        print("finally")


func()
