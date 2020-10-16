"""
Created on 16 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

requires pycryptodome

https://stackoverflow.com/questions/42568262/how-to-encrypt-text-with-a-password-in-python
"""

import base64
import sys

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from getpass import getpass


# --------------------------------------------------------------------------------------------------------------------

class Crypt(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def key_from_user():
        print("Enter password for encryption: ", file=sys.stderr)
        return getpass()


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def encrypt(key, plain_text):
        key_bytes = key.encode()
        source = plain_text.encode()

        key = SHA256.new(key_bytes).digest()                # use SHA-256 over our key to get a proper-sized AES key
        iv = Random.new().read(AES.block_size)              # generate IV
        encryptor = AES.new(key, AES.MODE_CBC, iv)

        padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
        source += bytes([padding]) * padding
        data = iv + encryptor.encrypt(source)               # store the IV at the beginning and encrypt

        return base64.b64encode(data).decode()


    @staticmethod
    def decrypt(key, cypher_text):
        key_bytes = key.encode()
        source = base64.b64decode(cypher_text.encode())

        key = SHA256.new(key_bytes).digest()                # use SHA-256 over our key to get a proper-sized AES key
        iv = source[:AES.block_size]                        # extract the IV from the beginning
        decrypter = AES.new(key, AES.MODE_CBC, iv)

        data = decrypter.decrypt(source[AES.block_size:])   # decrypt
        padding = data[-1]                                  # pick the padding value from the end

        if data[-padding:] != bytes([padding]) * padding:
            raise ValueError("invalid padding")

        return data[:-padding]                              # remove the padding
