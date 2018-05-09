import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(),'..'))
import uuid
from mainASBT import CommonASBT
import pickle
import socket

class TransactionClass(CommonASBT):
    """This class will be used by software provider to create a transaction"""
    def __init__(self, hostname, SW_FILE, DEST_PUB_KEY, DEST_DIG_SIG=None):
        super(TransactionClass, self).__init__()
        self.hostname = hostname
        self.sw_file_name = SW_FILE
        self.txn_id = uuid.uuid4()
        self.first_txn_id = uuid.uuid4()
        self.KEY_FILE_PATH = ''                     # directory location of public-private key
        self.KEY_FILE_NAME = 'mykey.pickle'         # to store the public-private key
        self.KEY_LENGTH = 1024
        self.TXN_POOL = 'txn_pool.pickle'           # to track the last transation id
        self.DEST_DIG_SIG = DEST_DIG_SIG
        self.DEST_PUB_KEY = DEST_PUB_KEY
        self.initializers()
    
    def initializers(self):
        """This method is to set all initializers"""
        self.get_my_key()                           # get or generate public-private key
        self.send_addr_pk_pair()                    # update the host public key
        # rename the software file
        # os.rename(self.sw_file_name, str(self.txn_id))
        # self.sw_file_name = str(self.txn_id)

    def get_my_key(self):
        """generate new key or if already exists then retrieve the key"""
        key_path = os.path.join(self.KEY_FILE_PATH,self.KEY_FILE_NAME)
        if not os.path.exists(key_path):
            self.key = self.get_key(self.KEY_LENGTH);
            self.save_keys(self.key, key_path)
        else:
            with open(key_path, 'rb') as key_file:
                self.key = pickle.load(key_file)
        
    def send_addr_pk_pair(self):
        """generate its own ip address public key pair"""
        addr_pk_pair = {self.get_ip_addr(self.hostname): self.key.publickey()}
        """send its public key to OBMs"""
        print('sendind its public key to OBM...')
        self.sendToSocket(self.get_ip_addr('h1'), 8085, (addr_pk_pair, 1))

    def rw_prev_txn_id(self):
        if os.path.exists(self.TXN_POOL):
            with open(self.TXN_POOL,'rb') as txn_pool:
                self.prev_txn_id = pickle.load(txn_pool)
        else:
            self.prev_txn_id = self.first_txn_id
            
        with open(self.TXN_POOL,'wb') as txn_pool:
            pickle.dump(self.txn_id, txn_pool)

    def read_sw_file(self):
        with open(self.sw_file_name, 'rb') as sw_file:
            self.sw_text = sw_file.read()

    def my_transaction(self):
        self.rw_prev_txn_id()                       # read-write previous transaction id
        self.read_sw_file()                         # read the content of software file
        plain_text = str(self.txn_id).encode() + str(self.prev_txn_id).encode() + self.sw_text
        hash_value = self.compute_hash(plain_text)
        self.pk1 = self.key.publickey()
        self.sign1 = self.digital_signature(self.key, hash_value)
        self.pk2 = self.DEST_PUB_KEY
        self.sign2 = self.DEST_DIG_SIG
        self.txn_packet = {'txn_id': self.txn_id, 'prev_txn_id': self.prev_txn_id, 'pk1': self.pk1, 'sign1': self.sign1, 'pk2': self.pk2, 'sign2': self.sign2}
        # self.pickle_txn()
        """  @S3  """
        """send this transaction packet to OBMs"""
        print('sending transaction packet to OBM...')
        self.sendToSocket(self.get_ip_addr('h1'), 8085, (self.txn_packet, 2))

    # def pickle_txn(self):
    #     with open('last_recent_txn.pickle', 'wb') as my_txn:
    #         pickle.dump(self.txn_packet, my_txn)

    def connectToSocket(self, ip, port):
        self.ss = socket.socket()  

    def sendToSocket(self, ip, port, packet):
        self.connectToSocket(ip, port)
        self.ss.connect((ip, port))
        data=pickle.dumps(packet)
        print("data prepare to send: ",packet)
        self.ss.send(data)

    def receiveToSocket(self, ip, port):
        self.connectToSocket(ip, port)
        self.ss.bind((ip, port))            # Bind to the port
        self.ss.listen(5)   
        while True:
            conn, addr = self.ss.accept()     # Establish connection with client.
            print('Got connection from', addr)
            data = conn.recv(1024)
            rcvd_data = pickle.loads(data)
            print(rcvd_data)
            self.get_sw_file(rcvd_data)    
            #print('Server received', repr(rcvd_data))
            # conn.send('Thank you for connecting')
            print("Operation Completed...")
            conn.close()



"""In order to create a transaction specify initials"""
HOSTNAME = 'h2'
software_file_name = 'OEM1_sw_upd8_v1.0'
# destination's public key
dest_pub_key_path = os.path.join('..','OEMs','mykey.pickle')
if os.path.exists(dest_pub_key_path):
    with open(dest_pub_key_path,'rb') as key_file:
        dest_key = pickle.load(key_file)
        dest_pub_key = dest_key.publickey()

TransactionClass(HOSTNAME, software_file_name, dest_pub_key).my_transaction()
