import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 12345)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)

while True:
    print ('waiting for msg')
    data, address = sock.recvfrom(1280)
    print ('received %s bytes from %s' % (len(data), address))
    print ('data is: ', data.decode())
    if data:
        sent = sock.sendto(data, address)
        print('sent %s bytes back to %s' % (sent, address))