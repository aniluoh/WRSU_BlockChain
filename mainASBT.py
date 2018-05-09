from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA 
from Crypto import Random
import pickle
import configparser
import os


class CommonASBT(object):
    """docstring for CommonASBT"""
    """important links: 
        1) https://alastairs-place.net/projects/netifaces/
        
    """
    def __init__(self):
        super(CommonASBT, self).__init__()
        self.KEY_LENGTH = 1024
        self.RAND_PARAM = 32

        self.rootDir = '..'
        self.subDir = 'config'
        self.ini_file = 'network.ini'
        self.section = 'mininet'
        self.config = configparser.ConfigParser()

    def get_ip_addr(self, hostname):
        # set ini file initialiser
        self.config.read(os.path.join(self.rootDir, self.subDir, self.ini_file))
        return self.config[self.section][hostname]
    
    def pkt_action(self, pkt_type):
        # set ini file initialiser
        self.config.read(os.path.join(self.rootDir, self.subDir, self.ini_file))
        return self.config[self.section][pkt_type]

    def get_key(self, key_length=None, rGen=True):
        # ARGUMENTS: 1) KEY_LENGTH, 2) RANDOM NUMBER GENERATOR
        if not key_length:
            key_length = self.KEY_LENGTH 
        if rGen:
            random_generator = Random.new().read
            key = RSA.generate(key_length, random_generator)
        else:
            key = RSA.generate(key_length)
        return key

    # WRITE DOWN PUBLIC AND PRIVATE KEY IN A FILE
    def save_keys(self, key, path):
        with open(path,'wb') as file:
            pickle.dump(key, file)
            # file.write(key.exportKey('PEM'))                # private key
            # file.write(b"\n")                               # new line in binary form
            # file.write(key.publickey().exportKey('PEM'))     # public key

    def encrypt_data(self, key, plain_text, random_param=None):
        # return cipherText
        # A matching RSA public key.
        if not random_param:
            random_param = self.RAND_PARAM
        public_key = key.publickey()
        cipherText = public_key.encrypt(plain_text, random_param)
        print("Encrypted data is : ", cipherText)
        return cipherText

    def decrypt_data(self, key, cipherText):
        # return plain_text
        plain_text = key.decrypt(cipherText)
        print("Decrypted data is ", plain_text)
        return plain_text

    def compute_hash(self, plain_text):
        hash_value = SHA256.new(plain_text).digest()
        return hash_value

    def digital_signature(self, key, hash_value):
        return key.sign(hash_value, '')

    def verify_signature(self, public_key, signature, hash_value):
        if(public_key.verify(hashB, Signature)):
            print("match")
            return 1
        else:
            print(" Not match")
            return 0

    def verify_both_signatures(self, pk1, sign1, pk2, sign2):
        if pk1.decrypt(sign1) == pk2.decrypt(sign2):
            return 1
        else:
            return 0

    def add_txn_block(self):
        print('Append new transaction into the BLOCK!')

# key = generate_key()
# print('key:\t',key)
# hashA = compute_hash("hello World!")
# print(repr(hashA))
# Signature = digital_signature(key, hashA)
# print("Digital Signatgure :" + repr(Signature) + "\n")
# hashB = compute_hash("hello World!")
# print("\n" + repr(hashB))
# verify_signature(key, Signature, hashA)

# print('public key:\t',key.publickey().exportKey('PEM'))
# public_key = key.publickey()

# print("key.can_encrypt",key.can_encrypt())
# print("key.can_sign",key.can_sign())
# #  Whether this is an RSA private key
# print("key.has_private",key.has_private())

