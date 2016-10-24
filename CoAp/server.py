import socket
import sys
from struct import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 12345)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)

def GET():
    print("GET Request")

def POST():
    print("POST Request")

def PUT():
    print("PUT Request")

def DELETE():
    print("DELETE Request")

options = {1: GET, 2: POST, 3: PUT, 4: DELETE}

def handleReq(header_option):
    code = (header_option[0] & 0x00FF0000) >> 16
    options[code]()

def unpackMsg(data):
    size = calcsize('!IB')
    return unpack('!IB', data[:size]), data[size:]

def packMsg():
    pass

def recvData():
    while True:
        print ('waiting for msg')
        data, address = sock.recvfrom(1280)
        print ('received %s bytes from %s' % (len(data), address))
        header_option, option_data = unpackMsg(data)

        handleReq(header_option)

        if data:
            sent = sock.sendto(data, address)
            print('sent %s bytes back to %s' % (sent, address))

def sendData():
    pass

recvData()