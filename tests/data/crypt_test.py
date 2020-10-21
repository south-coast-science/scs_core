#!/usr/bin/env python3

"""
Created on 16 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.crypt import Crypt


# --------------------------------------------------------------------------------------------------------------------

my_password = "secret_AES_key_string_to_encrypt/decrypt_with"
my_data = "input_string_to_encrypt/decrypt"

print("key:  {}".format(my_password))
print("data: {}".format(my_data))

encrypted = Crypt.encrypt(my_password, my_data)
print("\nenc:  {}".format(encrypted))

decrypted = Crypt.decrypt(my_password, encrypted)
print("dec:  {}".format(decrypted))
print("\ndata match: {}".format(my_data == decrypted))

print("\nSecond round....")
encrypted = Crypt.encrypt(my_password, my_data)
print("\nenc:  {}".format(encrypted))

print("\nwrong pass....")
my_password = "secret_AES_key_string_to_encrypt/decrypt"

decrypted = Crypt.decrypt(my_password, encrypted)
print("dec:  {}".format(decrypted))
print("\ndata match: {}".format(my_data == decrypted))
