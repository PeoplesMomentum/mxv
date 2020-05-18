from Crypto.Cipher import AES
import base64
import hashlib

# key or IV generation (from https://pypi.org/project/pycryptodome/): 
#
# from django.utils.crypto import get_random_string
# get_random_string(50)


# based on https://github.com/arajapandi/php-python-encrypt-decrypt
class SimpleEncryption:
    method = AES.MODE_CFB
    blocksize = 32
    pad_with = '`'

    # stores the IV and key
    def __init__(self, iv, key):
        if not iv or iv == '':
            raise Exception('SimpleEncryption: no iv')
        if not key or key == '':
            raise Exception('SimpleEncryption: no key')
        self.iv = iv
        self.key = key

    # pads a string to the next block size boundary
    def pad(self, s): return s + (self.blocksize - len(s) % self.blocksize) * self.pad_with

    # gets the first 32 hex of the hashed key
    def get_key(self):
        return hashlib.sha256(self.key.encode('utf-8')).hexdigest()[:32]

    # gets the first 16 hex of the hashed IV
    def get_iv(self):
        return hashlib.sha256(self.iv.encode('utf-8')).hexdigest()[:16]

    # returns the encrypted text
    def encrypt(self, raw):
        cipher = AES.new(self.get_key(), self.method, self.get_iv(), segment_size = 128)
        return base64.b64encode(cipher.encrypt(self.pad(raw)))

    # returns the raw text
    def decrypt(self, encrypted):
        cipher = AES.new(self.get_key(), self.method, self.get_iv(), segment_size = 128)
        return cipher.decrypt(base64.b64decode(encrypted)).decode('utf-8').rstrip(self.pad_with)