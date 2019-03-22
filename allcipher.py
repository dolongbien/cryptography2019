# -*- coding: utf-8 -*-

import os
import random
import struct
import hashlib
import zlib
import base64
from Crypto.Cipher import AES, DES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import config


class AllCipher():
    """ Encryption and decryption are done in chunksize to prevent running out
        of memory for large fales.
        For encryption AES (256bit) in CBC mode is used.
    """
    def __init__(self, password, infile, isRSA=False):
        if isRSA:
            #Import the Public Key and use for encryption using PKCS1_OAEP
            rsa_key = RSA.importKey(open(password).read())
            self.key = PKCS1_OAEP.new(rsa_key)
            self.chunksize = 512
        else:
            self.key = hashlib.sha256(password.encode('utf-8')).digest()
            self.chunksize = 64*1024

        self.infile = infile


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
        config.process_bar.setValue(100)
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
        config.process_bar.setRange(0,100)
        config.process_bar.setValue(0)

        tempfile = self.infile + ".tmp"

        with open(tempfile, 'rb') as infile:
            with open(self.infile, 'wb') as outfile:
                #compress the data first
                blob = zlib.compress(infile.read())

                #In determining the chunk size, determine the private key length used in bytes
                #and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
                #in chunks
                # 512 - 42 = 470
                chunk_size = self.chunksize - 42
                offset = 0
                end_loop = False
                encrypted = b""

                while not end_loop:
                    chunk = blob[offset:offset + chunk_size]

                    if len(chunk) % chunk_size != 0:
                        end_loop = True
                        chunk += b" " * (chunk_size - len(chunk))

                    encrypted += self.key.encrypt(chunk)

                    offset += chunk_size

                outfile.write(base64.b64encode(encrypted))

        config.process_bar.setValue(100)
        return True

    def decrypt_RSA(self):
        config.process_bar.setRange(0,100)
        config.process_bar.setValue(0)
        out_filename = os.path.splitext(self.infile)[0] + '.tar'
        with open(self.infile, 'rb') as infile:
            encrypted_blob = base64.b64decode(infile.read())

            #In determining the chunk size, determine the private key length used in bytes.
            #The data will be in decrypted in chunks
            offset = 0
            decrypted = b""

            #keep loop going as long as we have chunks to decrypt
            while offset < len(encrypted_blob):
                chunk = encrypted_blob[offset: offset + self.chunksize]

                #Append the decrypted chunk to the overall decrypted file
                decrypted += self.key.decrypt(chunk)

                offset += self.chunksize
        with open(out_filename, 'wb') as outfile:
            outfile.write(zlib.decompress(decrypted))
        config.process_bar.setValue(100)
        return out_filename


