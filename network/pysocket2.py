import socket
import os

address = ('127.0.0.1', 9999)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
f = open(os.path.join(os.getcwd(),'a.txt'), 'w+')

while True:
    data, addr = s.recvfrom(1024)
    print('data', data)
    f.write(data)
    f.flush()
f.close()
s.close()