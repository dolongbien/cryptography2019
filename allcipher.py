# -*- coding: utf-8 -*-

import os
import random
import struct
import hashlib
from Crypto.Cipher import AES, DES
import config


class AllCipher():
    """ Encryption and decryption are done in chunksize to prevent running out
        of memory for large fales.
        For encryption AES (256bit) in CBC mode is used.
    """
    def __init__(self, password, infile):
        self.key = hashlib.sha256(password.encode('utf-8')).digest()
        print(len(self.key))
        self.infile = infile
        self.chunksize = 64*1024

    def encrypt_AES(self):
        config.process_bar.setRange(0,100)
        config.process_bar.setValue(0)
        # 16 byte random IV  - initialization vector (IV)
        # the IV is as important as the salt in hashed passwords
        iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
        iv = iv.encode()[:16]
        print(len(self.key))
        encryptor = AES.new(self.key, AES.MODE_CBC, iv)
        tempfile = self.infile + ".tmp"
        filesize = os.path.getsize(tempfile)
        with open(tempfile, 'rb') as infile:
            with open(self.infile, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize)) # Q  unsigned long long
                # < little-endian
                # >   big-endian
                outfile.write(iv)
                while True:
                    chunk = infile.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        # padding to make data size divisible by 16
                        chunk += ' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))
        config.process_bar.setValue(50)
        return True

    def decrypt_AES(self):
        out_filename = os.path.splitext(self.infile)[0] + '.tar'
        with open(self.infile, 'rb') as infile:
            origsize = struct.unpack('<Q',
                                     infile.read(struct.calcsize('Q'))
                                     )[0]
            iv = infile.read(16)
            decryptor = AES.new(self.key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)
        return out_filename

    def encrypt_DES(self):
        config.process_bar.setRange(0,100)
        config.process_bar.setValue(0)
        iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(8)])
        iv = iv.encode()[:8]
        cipher = DES.new(self.key[:8], DES.MODE_OFB, iv)
        tempfile = self.infile + ".tmp"
        filesize = os.path.getsize(tempfile)
        with open(tempfile, 'rb') as infile:
            with open(self.infile, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize)) # Q  unsigned long long
                outfile.write(iv)             
                while True:
                    chunk = infile.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(cipher.encrypt(chunk))
        config.process_bar.setValue(100)
        return True

    def decrypt_DES(self):
        out_filename = os.path.splitext(self.infile)[0] + '.tar'
        with open(self.infile, 'rb') as infile:
            origsize = struct.unpack('<Q',
                                     infile.read(struct.calcsize('Q'))
                                     )[0]
            iv = infile.read(8)
            decryptor = DES.new(self.key[:8], DES.MODE_OFB, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))
                outfile.truncate(origsize)
        return out_filename

    def encrypt_RSA(self):
        pass
        # TODO

    def decrypt_RSA(self):
        pass
        # TODO