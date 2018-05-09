import os
import socket
import sys
sys.path.insert(0, os.path.join(os.getcwd(),'..'))
import uuid
from mainASBT import CommonASBT
import pickle


class TransactionClass(CommonASBT):
    """This class will be used by software provider to create a transaction"""
    def __init__(self, hostname):
        super(TransactionClass, self).__init__()
        self.KEY_FILE_PATH = ''
        self.KEY_FILE_NAME = 'mykey.pickle'
        self.hostname = hostname
        self.initializers()

    def initializers(self):
        self.get_my_key()
        self.send_addr_pk_pair()

    def get_my_key(self):
        key_path = os.path.join(self.KEY_FILE_PATH,self.KEY_FILE_NAME)
        if not os.path.exists(key_path):
            self.key = self.get_key();
            self.save_keys(self.key, key_path)
        else:
            with open(key_path, 'rb') as key_file:
                self.key = pickle.load(key_file)
        """in future implement change key"""

    def send_addr_pk_pair(self):
        """generate its own ip address public key pair"""
        addr_pk_pair = {self.get_ip_addr(self.hostname): self.key.publickey()}
        print(addr_pk_pair)
        """send its public key to OBMs"""
        print('sendind its public key to OBM...')
        self.sendToSocket(self.get_ip_addr('h1'), 8085, (addr_pk_pair, 1))

    """  @S5  """
    def cloud_sw_request(self, txn_packet):
        
        self.txn_packet = txn_packet
        self.sw_filename = 'OEM1_sw_upd8_v1.0'
        # request to software file to download
        self.sendToSocket(self.get_ip_addr('h4'), 8085, (self.sw_filename, 3))
    
    def read_sw_file(self):
        with open(self.sw_filename, 'rb') as sw_file:
            self.sw_text = sw_file.read()

    def cloud_download(self, sw_file_stream):
        
        sw_file = open(self.sw_filename, 'wb')
        sw_file.write(sw_file_stream)
        sw_file.close()

        self.mainOEM()

    def mainOEM(self):
        self.read_sw_file()
        plain_text = str(self.txn_packet['txn_id']).encode() + str(self.txn_packet['prev_txn_id']).encode() + self.sw_text
        hash_value = self.compute_hash(plain_text)

        if self.verify_signature(pk1, sign1, hash_value):
            self.txn_packet['sign2'] = self.digital_signature(self.key, hash_value)

        """send this updated transaction packet to OBMs"""
        print('send updated transaction packet to OBM')
        self.sendToSocket(self.get_ip_addr('h1'), 8085, (self.txn_packet,1))

    def connectToSocket(self, ip, port):
        self.ss = socket.socket()             # Create a socket object

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
            rcvd_data, pkt_type = pickle.loads(data)
            print(rcvd_data, pkt_type)
            if pkt_type == 2:
                self.cloud_sw_request(rcvd_data)
            elif pkt_type == 4:
                self.cloud_download(rcvd_data)
            else:
                print("wrong server request!")
            #print('Server received', repr(rcvd_data))
            # conn.send('Thank you for connecting')
            print("Operation Completed...")
            conn.close()
    
HOSTNAME = 'h3'    
software_file_name = 'OEM1_sw_upd8_v1.0'
TransactionClass(HOSTNAME).receiveToSocket('',8085)