import hashlib 
import datetime as dt
import pandas as pd
import sys
from struct import *


class BlockChain(object):
    """docstring for BlockChain"""
    def __init__(self, number_of_transactions=0, height=0, timestamp=dt.datetime.now(), previous_block=None, size=10):
        # super(BlockChain, self).__init__()
        #previous_Block means hash_of_previous transaction
        self.number_of_transactions = number_of_transactions
        self.height = height 
        self.timestamp = timestamp
        self.previous_block = previous_block
        self.size = size
        self.MAX_TXN = 5

    def total_transaction(self):
        with open('pool.txt','rb') as poolf:
            self.ttxn = poolf.read()
            print('self.ttxn:\t',self.ttxn)
            print('self.ttxn:\t',ord(self.ttxn))
        number_of_transactions = int.from_bytes(self.ttxn, byteorder='big') + 1
        
        print('Total number of transactions till now:\t',number_of_transactions)
        
        if number_of_transactions == self.MAX_TXN:
            self.create_block()
            number_of_transactions = 0
            # also node verify

        elif number_of_transactions > self.MAX_TXN:
            print('something went wrong!')
            number_of_transactions = 0
            print('number_of_transactions reset to zero')

        with open('pool.txt','wb') as poolf:
            poolf.write(number_of_transactions.to_bytes(2,byteorder='big'))
        return 1

    def transaction(self):
        if self.total_transaction() != 1:
            print('something is wrong!')
            sys.exit()   
        self.txn_id = dt.datetime.now().date()
        print(self.txn_id)
        self.pk_1 = None
        self.pk_1_sign = None
        self.pk_2 = None
        self.pk_2_sign = None
        # self.metadata.obm_id = None
        # self.metadata.cloud_pk = None
        # self.metadata.Auth_details = None
        return self.txn_id

    def create_genesis_block(self):
        df =  pd.DataFrame(["1","0",dt.datetime.now()," ","1"])
        previous_hash = 0
        self.hash = self.get_hash()
        current_hash = self.hash
        transaction_details = 'mymsg'
        print(df)
        return df

    def create_block(self):
        print('Block Formation!')


    def display(self):
        df = pd.DataFrame([self.number_of_transactions,self.height,self.timestamp, self.previous_block, self.size], columns=['number_of_transactions','height','timestamp','previous_block','size'])
        print(df)
        return df

    def get_hash(self):
        header_bin = (str(self.number_of_transactions)+str(self.height)+ str(self.timestamp)+ str(self.previous_block)).encode()
        
        self.inner_hash = hashlib.sha256(header_bin).hexdigest().encode()
        outer_hash = hashlib.sha256(header_bin).hexdigest()
        return outer_hash
        
BlockChain().transaction()
# block_chain = [BlockChain().create_genesis_block()]
# print("The genesis block has been created!")
# print("Hash: %s" %block_chain[-1].get_hash())
# block_chain[-1].display().to_csv('demo',',')