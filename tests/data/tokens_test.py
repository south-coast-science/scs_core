#!/usr/bin/env python3

"""
Created on 8 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.tokens import Tokens


# --------------------------------------------------------------------------------------------------------------------

key = Tokens.construct('a1/b1/c1/d1', '/')
print("key: %s" % key)
print("-")


text = 'a1/b1/c1/d1'
print(text)

prefix = Tokens.construct(text, '/')
print("prefix: %s" % prefix)

equals = key == prefix
print("key == prefix: %s" %  equals)
print("key startswith prefix: %s" % key.startswith(prefix))
print("-")


text = 'a1/b1/c1'
print(text)

prefix = Tokens.construct(text, '/')
print("prefix: %s" % prefix)

equals = key == prefix
print("key == prefix: %s" %  equals)
print("key startswith prefix: %s" % key.startswith(prefix))
print("-")


text = 'a1/b1/c1/'
print(text)

prefix = Tokens.construct(text, '/')
print("prefix: %s" % prefix)

print("key startswith prefix: %s" % key.startswith(prefix))
print("-")


text = 'a1/b2/c1'
print(text)

prefix = Tokens.construct(text, '/')
print("prefix: %s" % prefix)

print("key startswith prefix: %s" % key.startswith(prefix))
print("-")


text = 'a1/b1/c1/d1/e1'
prefix = Tokens.construct(text, '/')
print("prefix: %s" % prefix)

print("key startswith prefix: %s" % key.startswith(prefix))
print("-")


text = '/'
print(text)

prefix = Tokens.construct(text, '/')
print("prefix: %s" % prefix)

print("key startswith prefix: %s" % key.startswith(prefix))
print("-")


text = ''
print(text)

prefix = Tokens.construct(text, '/')
print("prefix: %s" % prefix)

print("key startswith prefix: %s" % key.startswith(prefix))
print("-")


text = None
print(text)

prefix = Tokens.construct(text, '/')
print("prefix: %s" % prefix)

print("key startswith prefix: %s" % key.startswith(prefix))
print("-")

