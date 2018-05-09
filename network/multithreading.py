#!/usr/bin/env python3

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import threading
import os
from time import sleep

def server(num=0):
    """
    server
    """
    import sys
    PORT_NUMBER = 5000
    SIZE = 1024

    hostName = gethostbyname( '0.0.0.0' )

    mySocket = socket( AF_INET, SOCK_DGRAM )
    mySocket.bind( (hostName, PORT_NUMBER) )

    print("Test server listening on port {0}\n".format(PORT_NUMBER))

    while True:
        sleep(.1)
        (data,addr) = mySocket.recvfrom(SIZE)
        print(data)
    sys.exit()
 
def client(SERVER_IP):
    """
    client
    """
    #!/usr/bin/env python3
    # SERVER_IP   = '10.0.0.1'
    PORT_NUMBER = 5000
    SIZE = 1024
    print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

    mySocket = socket( AF_INET, SOCK_DGRAM )
    myMessage = "Hello!"
    myMessage1 = ""
    i = 0
    while True:
        mySocket.sendto(myMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))
        i = i + 1
        sleep(.5)

    mySocket.sendto(myMessage1.encode('utf-8'),(SERVER_IP,PORT_NUMBER))

    sys.exit()

if __name__ == "__main__":
    # creating thread
    t2 = threading.Thread(target=server, args=(10,))
    t1 = threading.Thread(target=client, args=(sys.argv[1],))
 
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
 
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
 
    # both threads completely executed
    print("Done!")



