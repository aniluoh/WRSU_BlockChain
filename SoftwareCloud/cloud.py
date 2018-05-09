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
        self.hostname = hostname

    def get_sw_file(self, sw_filename):
        # software filename will be same as txn_packet['txn_id']
        sw_file = open(sw_filename, 'rb')
        return sw_file.read(1024)

    def cloud_main(self, sw_filename, requesters_addr):
        print('sending to address: ', requesters_addr)
        print(self.get_sw_file(sw_filename))
        self.sendToSocket(requesters_addr, 8085, (self.get_sw_file(sw_filename), 4))

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
            if pkt_type == 3:
                self.cloud_main(rcvd_data, addr[0])
            else:
                print("wrong server request!")
            print("Operation Completed...")
            conn.close()
    
HOSTNAME = 'h4'
TransactionClass(HOSTNAME).receiveToSocket('',8085)