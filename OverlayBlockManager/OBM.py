import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(),'..'))
import uuid
import socket    
from mainASBT import CommonASBT
import pickle


class TransactionClass(CommonASBT):
    """This class will be used by software provider to create a transaction"""
    def __init__(self, hostname):
        super(TransactionClass, self).__init__()
        self.hostname = hostname
        self.ADDR_PK_DICT = 'addr_key_table.pickle'
        self.KEY_FILE_PATH = ''
        self.KEY_FILE_NAME = 'mykey.pickle'
        self.KEY_LENGTH = 1024
        self.initializers()
    
    def initializers(self):
        """This method is to set all initializers"""
        self.get_my_key()
        # {IP_Addr: Public_key} PAIRS
        self.Addr_pk_table = {self.get_ip_addr(self.hostname): self.key.publickey()}
        # self.new_transaction()
        
    def get_my_key(self):
        """generate new key or if already exists then retrieve the key"""
        key_path = os.path.join(self.KEY_FILE_PATH,self.KEY_FILE_NAME)
        if not os.path.exists(key_path):
            self.key = self.get_key(self.KEY_LENGTH);
            self.save_keys(self.key, key_path)
        else:
            with open(key_path, 'rb') as key_file:
                self.key = pickle.load(key_file)
        """in future implement change key"""

    def read_addr_pk_table(self):
        if os.path.exists(self.addr_pk_path):
            with open(self.addr_pk_path, 'rb') as rpf:
                self.Addr_pk_table = pickle.load(rpf)
        
    """  @S2  """
    def update_addr_pk_table(self, new_ip_pk_map=None):
        """Public Key Address pairs
        Input args: 1) pass the {ip address: public key} pair (Dictionary)
        output:     1) update its address key table
        """
        # set address public key path
        self.addr_pk_path = os.path.join(os.getcwd(), self.ADDR_PK_DICT)
        # read address-public_key table
        self.read_addr_pk_table()
        # update the address-public_key table
        if new_ip_pk_map:
            # update the Address public key table
            self.Addr_pk_table.update(new_ip_pk_map)
            with open(self.addr_pk_path,  'wb') as wpf:
                pickle.dump(self.Addr_pk_table, wpf)
        print(self.Addr_pk_table)

    """  @S4  """
    def new_transaction(self, txn_packet=None):
        # with open(os.path.join(os.getcwd(),'..','SPs','last_recent_txn.pickle'), 'rb') as file:
        #     txn_packet = pickle.load(file)
        
        # get latest address-public_key table
        self.read_addr_pk_table()
        
        if txn_packet['sign2'] != None:
            """check the packet authenticity and add the transaction into the block"""
            print('Authenticating the packet...')
            if self.verify_both_signatures(pk1, sign1, pk2, sign2):
                """add transaction into the block and then broadcast"""
                print('Appending this transaction into the current BLOCK!...')
                """broadcast this transaction to the network"""

        else:
            IP_Found = 0
            print('Matching addr_key_table for forwarding the packet')
            for IP_Addr in self.Addr_pk_table:
                if txn_packet['pk2'] == self.Addr_pk_table[IP_Addr]:
                    print('Match Found!\t Destination IP_Addr is:', IP_Addr)
                    IP_Found = 1
                    break;        

            if IP_Found:
                """forward the transaction packet to respective IP Address"""
                print('Forwarding transaction packet to respective OEM\'s IP Address!', IP_Addr)
                self.sendToSocket(IP_Addr, 8085, (txn_packet, 2))

            else:
                """broadcast"""
                print('No Match Found!, broadcast the packet since publickey not present in this network')

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
            rcvd_data, pkt_type = pickle.loads(data)
            print(rcvd_data, pkt_type)
            if pkt_type == 1:
                self.update_addr_pk_table(rcvd_data)
            elif pkt_type == 2:
                self.new_transaction(rcvd_data)
            else:
                print("wrong server request!")
            #print('Server received', repr(rcvd_data))
            # conn.send('Thank you for connecting')
            print("Operation Completed...")
            conn.close()



HOSTNAME = 'h1'
TransactionClass(HOSTNAME).receiveToSocket('',8085)