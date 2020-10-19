"""
Created on 16 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

requires pycryptodome

https://stackoverflow.com/questions/42568262/how-to-encrypt-text-with-a-password-in-python
https://github.com/openthread/openthread/issues/1137
"""

from base64 import b64decode, b64encode

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


# --------------------------------------------------------------------------------------------------------------------

class Crypt(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def encrypt(key, plain_text):
        key_bytes = key.encode()
        source = plain_text.encode()

        long_key = SHA256.new(key_bytes).digest()           # use SHA-256 over our key to get a proper-sized AES key
        iv = Random.new().read(AES.block_size)              # generate IV
        encryptor = AES.new(long_key, AES.MODE_CBC, iv)

        padding = AES.block_size - len(source) % AES.block_size     # calculate required padding
        source += bytes([padding]) * padding
        data = iv + encryptor.encrypt(source)               # store the IV at the beginning and encrypt

        return b64encode(data).decode()


    @staticmethod
    def decrypt(key, cypher_text):
        key_bytes = key.encode()
        source = b64decode(cypher_text.encode())

        long_key = SHA256.new(key_bytes).digest()           # use SHA-256 over our key to get a proper-sized AES key
        iv = source[:AES.block_size]                        # extract the IV from the beginning
        decrypter = AES.new(long_key, AES.MODE_CBC, iv)

        data = decrypter.decrypt(source[AES.block_size:])   # decrypt
        padding = data[-1]                                  # extract the padding value from the end

        if data[-padding:] != bytes([padding]) * padding:
            raise KeyError(key)

        return data[:-padding].decode()                     # remove the padding
