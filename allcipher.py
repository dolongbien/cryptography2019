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
        # 16 byte random IV  - initialization vector (IV)
        # the IV is as important as the salt in hashed passwords
        iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
        iv = iv.encode()[:16]
        #print(len(self.key))
        encryptor = AES.new(self.key, AES.MODE_CBC, iv)
        tempfile = self.infile + ".tmp"
        filesize = os.path.getsize(tempfile)
        try:
        	config.process_bar.setValue(5)
        except:
        	pass

        with open(tempfile, 'rb') as infile:
            with open(self.infile, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize)) # Q  unsigned long long
                # < little-endian
                # >   big-endian
                outfile.write(iv)
                try:
                	config.process_bar.setValue(10)
                except:
                	pass
                i = 0
                #print(filesize)
                while True:
                	chunk = infile.read(self.chunksize)
                	i = i + 32
                	if len(chunk) == 0:
                		break
                	elif len(chunk) % 16 != 0:
                	# padding to make data size divisible by 16
                		chunk += ' ' * (16 - len(chunk) % 16)
                	outfile.write(encryptor.encrypt(chunk))
                	try:
                	# make sure process still less than 90
                		#print(10 + 80*(i + 1)//len(chunk))
                		config.process_bar.setValue(10 + 80*(i + 1)//len(chunk))  
                	except:
                		pass
            try:
            	config.process_bar.setValue(95)
            except:
            	pass
            return True

    def decrypt_AES(self):

        out_filename = os.path.splitext(self.infile)[0] + '.tar'
        print(out_filename)
        try:
            config.process_bar.setValue(5)
        except:
            pass
        with open(self.infile, 'rb') as infile:
            origsize = struct.unpack('<Q',
                                     infile.read(struct.calcsize('Q'))
                                     )[0]
            iv = infile.read(16)
            try:
                config.process_bar.setValue(10)
            except Exception as e:
                raise e
            decryptor = AES.new(self.key, AES.MODE_CBC, iv)
            i = 0
            with open(out_filename, 'wb') as outfile:
                while True:
                    i = i + 32
                    chunk = infile.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))
                    try:
                        config.process_bar.setValue(10+80*(i+1)//len(chunk))
                    except Exception as e:
                        raise e
                outfile.truncate(origsize)
            try:
                config.process_bar.setValue(95)
            except Exception as e:
                raise e
        return out_filename

    def encrypt_DES(self):

        iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(8)])
        iv = iv.encode()[:8]
        cipher = DES.new(self.key[:8], DES.MODE_OFB, iv)
        tempfile = self.infile + ".tmp"
        filesize = os.path.getsize(tempfile)
        try:
            config.process_bar.setValue(5)
        except Exception as e:
            pass

        with open(tempfile, 'rb') as infile:
            with open(self.infile, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize)) # Q  unsigned long long
                outfile.write(iv)  
                i = 0           
                while True:
                    i = i + 32
                    chunk = infile.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(cipher.encrypt(chunk))
                    try:
                        config.process_bar.setValue(10 + 80*(i+1)//len(chunk))
                    except Exception as e:
                        raise e
        try:
            config.process_bar.setValue(95)
        except Exception as e:
            pass
        return True

    def decrypt_DES(self):

        out_filename = os.path.splitext(self.infile)[0] + '.tar'
        try:
            config.process_bar.setValue(5)
        except Exception as e:
            raise e
        with open(self.infile, 'rb') as infile:
            origsize = struct.unpack('<Q',
                                     infile.read(struct.calcsize('Q'))
                                     )[0]
            iv = infile.read(8)
            decryptor = DES.new(self.key[:8], DES.MODE_OFB, iv)
            i = 0 
            with open(out_filename, 'wb') as outfile:
                while True:
                    i = i + 32
                    chunk = infile.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))
                    try:
                        config.process_bar.setValue(10 + 80*(i+1)//len(chunk))
                    except Exception as e:
                        raise e
                outfile.truncate(origsize)
        try:
            config.process_bar.setValue(95)
        except Exception as e:
            raise e
        return out_filename

    def encrypt_RSA(self):

        tempfile = self.infile + ".tmp"
        try:
            config.process_bar.setValue(5)
        except Exception as e:
            raise e
        with open(tempfile, 'rb') as infile:
            with open(self.infile, 'wb') as outfile:
                #compress the data first
                blob = zlib.compress(infile.read())
                try:
                    config.process_bar.setValue(10)
                except Exception as e:
                    raise e
                #In determining the chunk size, determine the private key length used in bytes
                #and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
                #in chunks
                # 512 - 42 = 470
                chunk_size = self.chunksize - 42
                offset = 0
                end_loop = False
                encrypted = b""
                i = 0

                while not end_loop:
                    chunk = blob[offset:offset + chunk_size]
                    i = i + 3
                    if len(chunk) % chunk_size != 0:
                        end_loop = True
                        chunk += b" " * (chunk_size - len(chunk))

                    encrypted += self.key.encrypt(chunk)

                    offset += chunk_size
                    try:
                        config.process_bar.setValue(10 + 80*(i+1)//len(chunk))
                    except Exception as e:
                        raise e

                outfile.write(base64.b64encode(encrypted))

        try:
            config.process_bar.setValue(95)
        except Exception as e:
            raise e
        return True

    def decrypt_RSA(self):

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


